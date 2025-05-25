from django.shortcuts import render
from .models import Issue, Log, IssueBin, Occurrence
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.decorators import parser_classes
from .parsers import *
import json
import datetime


def home(request):
    return render(request, "home.html")


def ticket(request, id):
    args = Issue.objects.get(id=id)
    return render(request, "ticket.html", {"args": args})

###########APIs###################


#@api_view(['GET', 'POST', 'DELETE'])
@api_view(['GET', 'POST'])
def RestProjects(request):
    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    events = IssueBin.objects.all()
    serializer = ProjectSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@parser_classes([TextParser, JSONUTF8Parser])
def RestIssues(request, bin_name):
    binID = IssueBin.objects.get(project_name=bin_name)
    if request.method == 'POST':
        if request.content_type == "text/plain; charset=utf-8":
            data = IssueBin.filterLog(str(request.data, encoding="utf-8").split('\n'))  # Get a list of relevant lines
        elif request.content_type == "application/json; charset=utf-8":
            data = IssueBin.filterLog(json.loads(str(request.data, encoding="utf-8").encode('unicode-escape').decode()).log_raw).split('\n')  # there is some formating issue here
        raw_log = '\n'.join(data.values())
        ref = Issue.retRelatedIssue(raw_log)
        if ref == -1:
            newIssue = Issue(project=binID, log_raw=raw_log)
            newIssue.save()
            newOccurrence = Occurrence(Issue=newIssue)
            newOccurrence.save()
            for key, value in data.items():
                a = Log(Issue=newIssue, line_number=key, line_raw=value)
                a.save()
        else:
            newOccurrence = Occurrence(Issue=Issue.objects.get(id=ref))
            newOccurrence.save()
        return Response(raw_log, content_type="text/plain; charset=utf-8")
    #events = Issue.objects.all()
    events = binID.issue_set.all()
    serializer = IssueSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PATCH'])
def RestIssueByID(request, bin_name, issue_id):
    item = Issue.objects.get(id=issue_id)
    if request.method == 'DELETE':
        item.delete()
        return Response("Issue #"+str(issue_id)+" deleted")
    if request.method == 'Patch':
        if request.data.status in Issue.STATUS_OPTIONS.keys():
            item.status = request.data.status
            return Response("Issue #" + str(issue_id) + " updated")
    serializer = IssueSerializer(item)
    return Response(serializer.data)


@api_view(['GET'])
def RestLog(request, bin_name, issue_id):
    item = Log.objects.all()
    serializer = LogSerializer(item, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def RestLogByID(request, bin_name, issue_id, log_id):
    item = Issue.objects.get(id=issue_id).log_set.get(id=log_id)
    #item = Log.objects.get(id=log_id)
    serializer = LogSerializer(item)
    return Response(serializer.data)


@api_view(['GET'])
def RestLogByID_time(request, bin_name, issue_id, log_id):
    # this is reall backwards and I'm leaving it in as more of a conversation piece.
    # I full understand that the point was to split the log and parse date from substring
    events = Issue.objects.get(id=issue_id).occurrence_set.all()
    serializer = OccurrenceSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def RestLogByID_line(request, bin_name, issue_id, log_id):
    item = Log.objects.get(id=log_id).line_number
    return Response(item)
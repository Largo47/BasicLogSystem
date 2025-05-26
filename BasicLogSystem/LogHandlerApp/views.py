from django.shortcuts import render
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework.views import APIView

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

def api(request):
    return render(request, "api.html")

def projects(request):
    args = IssueBin.objects.all()
    return render(request, "projects.html", {"args": args})


def project_tickets(request, bin_name):
    args = IssueBin.objects.get(project_name=bin_name).issue_set.all()
    name = IssueBin.objects.get(project_name=bin_name).project_name
    return render(request, "project_tickets.html", {"args": args, "name": name})


def ticket(request, issue_id, bin_name):
    args = IssueBin.objects.get(project_name=bin_name).issue_set.get(id=issue_id)
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
@parser_classes([TextParser, JSONParser, FileUploadParser])
def RestIssues(request, bin_name, filename=None):
    binID = IssueBin.objects.get(project_name=bin_name)
    if request.method == 'POST':
        if request.content_type == "text/plain; charset=utf-8":
            data = IssueBin.filterLog(str(request.data, encoding="utf-8").split('\n'))  # Get a list of relevant lines
        elif request.content_type == "application/json":
            data = IssueBin.filterLog(json.loads(str(request.data).encode('unicode-escape').decode()).log_raw).split('\n')
            # there is some formating issue here
        elif request.content_type == "*/*":  # and filename != None:
            file_obj = request.data['file']
            data = IssueBin.filterLog(LogFile.getLogFromFile(file_obj))
        else:
            return Response("Incorrect data in request")
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
    events = binID.issue_set.all()
    serializer = IssueSerializer(events, many=True)
    return Response(serializer.data)

#class UploadLog(APIView):

@api_view(['GET', 'DELETE', 'PATCH'])
def RestIssueByID(request, bin_name, issue_id):
    item = Issue.objects.get(id=issue_id)
    if request.method == 'DELETE':
        item.delete()
        return Response("Issue #"+str(issue_id)+" deleted")
    if request.method == 'PATCH':
        if request.data['status'] in Issue.STATUS_OPTIONS.keys():
            item.status = request.data["status"]
            item.save()
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
    # this is really backwards and I'm leaving it in as more of a conversation piece.
    # I full understand that the point was to split the log and parse date from substring
    events = Issue.objects.get(id=issue_id).occurrence_set.all()
    serializer = OccurrenceSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def RestLogByID_line(request, bin_name, issue_id, log_id):
    item = Log.objects.get(id=log_id).line_number
    return Response(item)


from django.shortcuts import render
from .models import Issue, Log, IssueBin, Occurrence
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.decorators import parser_classes
from .parsers import TextParser
import datetime


def home(request):
    return render(request, "home.html")


def ticket(request, id):
    args = Issue.objects.get(id=id)
    return render(request, "ticket.html", {"args": args})

###########APIs###################


@api_view(['GET'])
def getTickets(request):
    tickets = Issue.objects.all()
    serializer = IssueSerializer(tickets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getLogs(request):
    logs = Log.objects.all()
    serializer = LogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOccurrence(request):
    events = Occurrence.objects.all()
    serializer = OccurrenceSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addTicket(request):
    serializer = IssueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([TextParser])
def addLog(request, binID=IssueBin.objects.get(id=1)):
    data = IssueBin.filterLog(str(request.data, encoding="utf-8").split('\n'))  # Get a list of relevant lines
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
    return Response(raw_log)

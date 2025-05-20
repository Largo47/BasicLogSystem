from django.shortcuts import render
from .models import Issue, Log, IssueBin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LogSerializer, IssueSerializer
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

@api_view(['POST'])
def addTicket(request):
    serializer = IssueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes([TextParser])
def addLog(request):
    data = IssueBin.filterLog(str(request.data, encoding="utf-8").split('\n'))  # Get a list of relevant lines
    raw_log = '\n'.join(data.values())
    #for item in data:

    newLog = Log(Issue=Issue.retRelatedIssue(raw_log), log_time=datetime.datetime.now(), log_raw=raw_log)
    newLog.save()
    return Response(LogSerializer(newLog).data)

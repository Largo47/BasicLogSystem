from django.shortcuts import render
from .models import Issue, Log
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LogSerializer, IssueSerializer
from rest_framework.decorators import parser_classes
from .parsers import TextParser

########
import datetime


def home(request):
    return render(request, "home.html")


def ticket(request, id):
    args = Issue.objects.get(id=id)
    return render(request, "ticket.html", {"args": args})

@api_view(['GET'])
def getData(request):
    logs = Log.objects.all()
    tickets = Issue.objects.all()
    serializer = LogSerializer(logs, many=True)
    serializer2 = IssueSerializer(tickets, many=True)
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
    data = request.data
    newLog = Log(Issue=Issue.objects.get(id=1), log_time = datetime.date.today(), log_raw = str(data))
    newLog.save()
    return Response(LogSerializer(newLog).data)

#from django.http import HttpResponse
from django.shortcuts import render
from .models import Issue, Log


def home(request):
    return render(request, "home.html")

def ticket(request, id):
    args = Issue.objects.get(id=id)
    return render(request, "ticket.html", {"args": args})

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ticket/<int:id>", views.ticket, name="ticket"),

    ##### APIs ######

    path('api/ticket/get/', views.getTickets, name='Get data'),
    path('api/log/get/', views.getLogs, name='Get data'),
    path('api/ticket/post/', views.addTicket, name='Add Ticket'),
    path('api/<str:bin_name>/log/post/', views.addLog, name='Add Log'),
]

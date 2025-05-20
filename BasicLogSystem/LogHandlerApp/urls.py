from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:id>", views.ticket, name="ticket"),

    ##### APIs ######

    path('get/ticket/', views.getTickets, name='Get data'),
    path('get/log/', views.getLogs, name='Get data'),
    path('post/ticket/', views.addTicket, name='Add Ticket'),
    path('post/log/', views.addLog, name='Add Log'),
]

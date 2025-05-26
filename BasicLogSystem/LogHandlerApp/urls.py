from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", views.api, name="api list"),
    path("projects/", views.projects, name="All projects"),
    path("projects/<str:bin_name>/", views.project_tickets, name="Project"),
    path("projects/<str:bin_name>/issues/<int:issue_id>", views.ticket, name="Issue"),

    ##### APIs ######
    path('api/projects', views.RestProjects, name='Projects'),
    path('api/projects/<str:bin_name>/issues', views.RestIssues, name='Ticket'),
    path('api/projects/<str:bin_name>/issues/<int:issue_id>', views.RestIssueByID, name='Ticket'),
    path('api/projects/<str:bin_name>/issues/<int:issue_id>/logs', views.RestLog, name='Logs'),
    path('api/projects/<str:bin_name>/issues/<int:issue_id>/logs/<int:log_id>', views.RestLogByID, name='Logs'),
    path('api/projects/<str:bin_name>/issues/<int:issue_id>/logs/<int:log_id>/datetime', views.RestLogByID_time, name='Logs'),
    path('api/projects/<str:bin_name>/issues/<int:issue_id>/logs/<int:log_id>/line', views.RestLogByID_line, name='Logs'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

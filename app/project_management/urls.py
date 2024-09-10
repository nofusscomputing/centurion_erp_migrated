from django.urls import path

from .views import project
from .views.project_task import ProjectTaskAdd, ProjectTaskChange, ProjectTaskDelete, ProjectTaskView

from core.views import ticket, ticket_comment


app_name = "Project Management"
urlpatterns = [
    path('', project.Index.as_view(), name='Projects'),

    path("project/add", project.Add.as_view(), name="_project_add"),
    path("project/<int:pk>", project.View.as_view(), name="_project_view"),
    path("project/<int:pk>/edit", project.Change.as_view(), name="_project_change"),
    path("project/<int:pk>/delete", project.Delete.as_view(), name="_project_delete"),

    path('project/<int:project_id>/<str:ticket_type>/add', ticket.Add.as_view(), name="_project_task_add"),
    path('project/<int:project_id>/<str:ticket_type>/<int:pk>/edit', ticket.Change.as_view(), name="_project_task_change"),
    path('project/<int:project_id>/<str:ticket_type>/<int:pk>/delete', ticket.Delete.as_view(), name="_project_task_delete"),
    path('project/<int:project_id>/<str:ticket_type>/<int:pk>', ticket.View.as_view(), name="_project_task_view"),

    path('project/<int:project_id>/<str:ticket_type>/<int:ticket_id>/comment/add', ticket_comment.Add.as_view(), name="_project_task_comment_add"),
    path('project/<int:project_id>/<str:ticket_type>/<int:ticket_id>/comment/<int:pk>/edit', ticket_comment.Change.as_view(), name="_project_task_comment_change"),
    path('project/<int:project_id>/<str:ticket_type>/<int:ticket_id>/comment/<int:parent_id>/add', ticket_comment.Add.as_view(), name="_project_task_comment_add"),


]

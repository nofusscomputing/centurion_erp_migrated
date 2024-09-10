from django.urls import path

from .views.project import ProjectIndex, ProjectAdd, ProjectDelete, ProjectChange, ProjectView
from .views.project_task import ProjectTaskAdd, ProjectTaskChange, ProjectTaskDelete, ProjectTaskView

app_name = "Project Management"
urlpatterns = [
    path('', project.Index.as_view(), name='Projects'),

    path("project/add", project.Add.as_view(), name="_project_add"),
    path("project/<int:pk>", project.View.as_view(), name="_project_view"),
    path("project/<int:pk>/edit", project.Change.as_view(), name="_project_change"),
    path("project/<int:pk>/delete", project.Delete.as_view(), name="_project_delete"),

    path("project/<int:pk>/task/add", ProjectTaskAdd.as_view(), name="_project_task_add"),
    path("project/<int:project_id>/task/<int:pk>/edit", ProjectTaskChange.as_view(), name="_project_task_change"),
    path("project/<int:project_id>/task/<int:pk>/delete", ProjectTaskDelete.as_view(), name="_project_task_delete"),
    path("project/<int:project_id>/task/<int:pk>", ProjectTaskView.as_view(), name="_project_task_view"),


]

from django.urls import path

from .views.project import ProjectIndex, ProjectAdd, ProjectChange, ProjectView


app_name = "Project Management"
urlpatterns = [
    path('', ProjectIndex.as_view(), name='Projects'),

    path("project/add", ProjectAdd.as_view(), name="_project_add"),
    path("project/<int:pk>", ProjectView.as_view(), name="_project_view"),
    path("project/<int:pk>/edit", ProjectChange.as_view(), name="_project_change"),
    
]

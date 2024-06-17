from django.urls import path

from .views.project import ProjectIndex, ProjectAdd, ProjectView


app_name = "Project Management"
urlpatterns = [
    path('', ProjectIndex.as_view(), name='Projects'),

    path("project/add", ProjectAdd.as_view(), name="_project_add"),
    
]

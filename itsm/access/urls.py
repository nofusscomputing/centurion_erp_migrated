from django.urls import path

from . import views

app_name = "Access"
urlpatterns = [
    path("", views.IndexView.as_view(), name="Organizations"),
    path("<int:pk>/", views.OrganizationView.as_view(), name="_organization"),
    path("<int:pk>/edit", views.OrganizationChange.as_view(), name="_organization_change"),
    path("<int:organization_id>/team/<int:pk>/", views.TeamView.as_view(), name="_team"),
    path("<int:pk>/team/add", views.TeamAdd.as_view(), name="_team_add"),
    path("<int:organization_id>/team/<int:pk>/edit", views.TeamChange.as_view(), name="_team_change"),
    path("<int:organization_id>/team/<int:pk>/delete", views.TeamDelete.as_view(), name="_team_delete"),
]

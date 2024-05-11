from django.urls import path

from . import views

app_name = "Access"
urlpatterns = [
    path("", views.IndexView.as_view(), name="Organizations"),
    path("<int:organization_id>/", views.OrganizationView.as_view(), name="_organization"),
    path("<int:organization_id>/team/<int:team_id>/", views.TeamView.as_view(), name="_team"),
]

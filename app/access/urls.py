from django.urls import path

from . import views
from .views import team, organization, user

app_name = "Access"
urlpatterns = [
    path("", organization.IndexView.as_view(), name="Organizations"),
    path("<int:pk>/", organization.View.as_view(), name="_organization_view"),
    # path("<int:pk>/edit", organization.Change.as_view(), name="_organization_change"),
    path("<int:organization_id>/team/<int:pk>/", team.View.as_view(), name="_team_view"),
    path("<int:pk>/team/add", team.Add.as_view(), name="_team_add"),
    path("<int:organization_id>/team/<int:pk>/delete", team.Delete.as_view(), name="_team_delete"),
    path("<int:organization_id>/team/<int:pk>/user/add", user.Add.as_view(), name="_team_user_add"),
    path("<int:organization_id>/team/<int:team_id>/user/<int:pk>/delete", user.Delete.as_view(), name="_team_user_delete"),
]

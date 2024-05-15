from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import access, index


urlpatterns = [
    path("", index.IndexView.as_view(), name='_api_home'),
    path("organization/", access.OrganizationList.as_view(), name='_api_orgs'),
    path("organization/<int:pk>/", access.OrganizationDetail.as_view(), name='_api_organization'),
    path("organization/<int:organization_id>/team/<int:group_ptr_id>/", access.TeamDetail.as_view(), name='_api_team'),
    path("organization/team/", access.TeamList.as_view(), name='_api_teams'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

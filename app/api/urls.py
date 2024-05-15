from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import access, index

from .views.itam import device as itam_device, software as itam_software, config as itam_config

urlpatterns = [
    path("", index.IndexView.as_view(), name='_api_home'),
    path("organization/", access.OrganizationList.as_view(), name='_api_orgs'),
    path("organization/<int:pk>/", access.OrganizationDetail.as_view(), name='_api_organization'),
    path("organization/<int:organization_id>/team/<int:group_ptr_id>/", access.TeamDetail.as_view(), name='_api_team'),
    path("organization/team/", access.TeamList.as_view(), name='_api_teams'),


    path("config/<str:device_name>/", itam_config.View.as_view(), name="_api_device_config"),

    path("device/", itam_device.List.as_view(), name="_api_devices"), 
    path("device/<int:pk>/", itam_device.Detail.as_view(), name="_api_device_view"),

    path("software/", itam_software.List.as_view(), name="_api_softwares"),
    path("software/<int:pk>/", itam_software.Detail.as_view(), name="_api_software_view"),

]

urlpatterns = format_suffix_patterns(urlpatterns)

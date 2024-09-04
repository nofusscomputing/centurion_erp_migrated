from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import access, config, index

from api.views.settings import permissions
from api.views.settings import index as settings

from api.views import assistance, itim
from api.views.core import tickets as core_tickets
from api.views.core import ticket_comments as core_ticket_comments

from .views.itam import software, config as itam_config
from .views.itam.device import DeviceViewSet
from .views.itam import inventory


app_name = "API"


router = DefaultRouter(trailing_slash=False)

router.register('', index.Index, basename='_api_home')

router.register('assistance/(?P<ticket_type>request)', core_tickets.View, basename='_api_assistance_request')
router.register('assistance/(?P<ticket_type>request)/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_assistance_request_ticket_comments')

router.register('device', DeviceViewSet, basename='device')

router.register('itim/(?P<ticket_type>change)', core_tickets.View, basename='_api_itim_change')
router.register('itim/(?P<ticket_type>change)/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_itim_change_ticket_comments')

router.register('itim/(?P<ticket_type>incident)', core_tickets.View, basename='_api_itim_incident')
router.register('itim/(?P<ticket_type>incident)/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_itim_incident_ticket_comments')

router.register('itim/(?P<ticket_type>problem)', core_tickets.View, basename='_api_itim_problem')
router.register('itim/(?P<ticket_type>problem)/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_itim_problem_ticket_comments')

router.register('software', software.SoftwareViewSet, basename='software')



urlpatterns = [

    path("assistance", assistance.index.Index.as_view(), name="_api_assistance"),

    #
    # Sof Old Paths to be refactored
    #

    path("config/<slug:slug>/", itam_config.View.as_view(), name="_api_device_config"),

    path("configuration/", config.ConfigGroupsList.as_view(), name='_api_config_groups'),
    path("configuration/<int:pk>", config.ConfigGroupsDetail.as_view(), name='_api_config_group'),

    path("device/inventory", inventory.Collect.as_view(), name="_api_device_inventory"),

    path("itim", itim.index.Index.as_view(), name="_api_itim"),

    path("organization/", access.OrganizationList.as_view(), name='_api_orgs'),
    path("organization/<int:pk>/", access.OrganizationDetail.as_view(), name='_api_organization'),
    path("organization/<int:organization_id>/team", access.TeamList.as_view(), name='_api_organization_teams'),
    path("organization/<int:organization_id>/team/<int:group_ptr_id>/", access.TeamDetail.as_view(), name='_api_team'),
    path("organization/<int:organization_id>/team/<int:group_ptr_id>/permissions", access.TeamPermissionDetail.as_view(), name='_api_team_permission'),
    path("organization/team/", access.TeamList.as_view(), name='_api_teams'),

    path("settings", settings.View.as_view(), name='_settings'),
    path("settings/permissions", permissions.View.as_view(), name='_settings_permissions'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls

from django.conf import settings as django_settings

from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import access, config, index

from api.views.settings import permissions
from api.views.settings import index as settings

from api.views import assistance, itim, project_management
from api.views.assistance import request_ticket
from api.views.core import (
    ticket_categories, 
    ticket_comment_categories,
    ticket_comments as core_ticket_comments
)
from api.views.itim import change_ticket, incident_ticket, problem_ticket
from api.views.project_management import (
    projects,
    project_milestone,
    project_state,
    project_type,
    project_task
)

from .views.itam import software, config as itam_config
from .views.itam.device import DeviceViewSet
from .views.itam import inventory


from api.v2.views import index as v2

from api.v2.views.assistance import (
    index as assistance_index_v2,
    request as request_ticket_v2,
    request_comments as request_comments_v2,
    ticket_linked_item as ticket_linked_item_v2,
    related_ticket as related_ticket_v2
)


from api.v2.views.itam import (
    index as itam_index_v2,
    device as device_v2,
    device_software as device_software_v2
)
from api.v2.views.settings import (
    index as settings_index_v2,
    device_model as device_model_v2,
    external_link as external_link_v2
)

from api.v2.views.itim import (
    service_device as service_device_v2
)

from api.v2.views.access import (
    organization as organization_v2
)


app_name = "API"


router = DefaultRouter(trailing_slash=False)

router.register('', index.Index, basename='_api_home')

router.register('assistance/request', request_ticket.View, basename='_api_assistance_request')
router.register('assistance/request/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_assistance_request_ticket_comments')

router.register('device', DeviceViewSet, basename='device')

router.register('itim/change', change_ticket.View, basename='_api_itim_change')
router.register('itim/change/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_itim_change_ticket_comments')

router.register('itim/incident', incident_ticket.View, basename='_api_itim_incident')
router.register('itim/incident/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_itim_incident_ticket_comments')

router.register('itim/problem', problem_ticket.View, basename='_api_itim_problem')
router.register('itim/problem/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_itim_problem_ticket_comments')

router.register('project_management/projects', projects.View, basename='_api_projects')
router.register('project_management/projects/(?P<project_id>[0-9]+)/milestones', project_milestone.View, basename='_api_project_milestone')
router.register('project_management/projects/(?P<project_id>[0-9]+)/tasks', project_task.View, basename='_api_project_tasks')
router.register('project_management/projects/(?P<project_id>[0-9]+)/tasks/(?P<ticket_id>[0-9]+)/comments', core_ticket_comments.View, basename='_api_project_tasks_comments')

router.register('settings/ticket_categories', ticket_categories.View, basename='_api_ticket_category')

router.register('settings/project_state', project_state.View, basename='_api_project_state')
router.register('settings/project_type', project_type.View, basename='_api_project_type')
router.register('settings/ticket_comment_categories', ticket_comment_categories.View, basename='_api_ticket_comment_category')

router.register('software', software.SoftwareViewSet, basename='software')


# API V2
if django_settings.API_TEST:

    router.register('v2', v2.Index, basename='_api_v2_home')

    router.register('v2/access', itam_index_v2.Index, basename='_api_v2_access_home')
    router.register('v2/access/organization', organization_v2.ViewSet, basename='_api_v2_organization')

    router.register('v2/assistance', assistance_index_v2.Index, basename='_api_v2_assistance_home')
    router.register('v2/assistance/ticket/request', request_ticket_v2.ViewSet, basename='_api_v2_ticket_request')
    router.register('v2/assistance/ticket/request/(?P<ticket_id>[0-9]+)/comments', request_comments_v2.ViewSet, basename='_api_v2_assistance_request_ticket_comments')
    router.register('v2/assistance/ticket/request/(?P<ticket_id>[0-9]+)/comments/(?P<parent_id>[0-9]+)/threads', request_comments_v2.ViewSet, basename='_api_v2_assistance_request_ticket_comment_threads')
    router.register('v2/assistance/ticket/request/(?P<ticket_id>[0-9]+)/linked_items', ticket_linked_item_v2.ViewSet, basename='_api_v2_ticket_linked_item')
    router.register('v2/assistance/ticket/request/(?P<ticket_id>[0-9]+)/related_tickets', related_ticket_v2.ViewSet, basename='_api_v2_related_ticket')


    router.register('v2/itam', itam_index_v2.Index, basename='_api_v2_itam_home')
    router.register('v2/itam/device', device_v2.ViewSet, basename='_api_v2_device')
    router.register('v2/itam/device/(?P<device_id>[0-9]+)/device_software', device_software_v2.ViewSet, basename='_api_v2_device_software')
    router.register('v2/itam/device/(?P<device_id>[0-9]+)/service', service_device_v2.ViewSet, basename='_api_v2_service_device')

    router.register('v2/settings', settings_index_v2.Index, basename='_api_v2_settings_home')
    router.register('v2/settings/device_model', device_model_v2.ViewSet, basename='_api_v2_device_model')
    router.register('v2/settings/external_link', external_link_v2.ViewSet, basename='_api_v2_external_link')


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

    path("project_management", project_management.index.Index.as_view(), name="_api_project_management"),

    path("settings", settings.View.as_view(), name='_settings'),
    path("settings/permissions", permissions.View.as_view(), name='_settings_permissions'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls

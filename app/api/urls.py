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


from api.viewsets import (
    index as v2
)

from access.viewset import (
    index as access_v2
)

from assistance.viewset import (
    index as assistance_index_v2
)

from config_management.viewset import (
    index as config_management_v2
)

from itim.viewsets import (
    index as itim_v2
)

from project_management.viewsets import (
    index as project_management_v2
)

from settings.viewsets import (
    index as settings_index_v2,
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
router.register('v2', v2.Index, basename='_api_v2_home')

router.register('v2/access', access_v2.Index, basename='_api_v2_access_home')

router.register('v2/assistance', assistance_index_v2.Index, basename='_api_v2_assistance_home')

router.register('v2/itim', itim_v2.Index, basename='_api_v2_itim_home')

router.register('v2/config_management', config_management_v2.Index, basename='_api_v2_config_management_home')

router.register('v2/project_management', project_management_v2.Index, basename='_api_v2_project_management_home')

router.register('v2/settings', settings_index_v2.Index, basename='_api_v2_settings_home')

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

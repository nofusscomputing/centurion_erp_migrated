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

from app.viewsets.base import (
    index as base_index_v2,
    content_type as content_type_v2,
    permisson as permission_v2,
    user as user_v2
)

from access.viewsets import (
    index as access_v2,
    organization as organization_v2,
    team as team_v2,
    team_user as team_user_v2
)

from assistance.viewsets import (
    index as assistance_index_v2,
    knowledge_base as knowledge_base_v2,
    knowledge_base_category as knowledge_base_category_v2
)

from config_management.viewsets import (
    index as config_management_v2,
    config_group as config_group_v2,
    config_group_software as config_group_software_v2
)

from itam.viewsets import (
    index as itam_index_v2,
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
router.register('v2/access/organization', organization_v2.ViewSet, basename='_api_v2_organization')
router.register('v2/access/organization/(?P<organization_id>[0-9]+)/team', team_v2.ViewSet, basename='_api_v2_organization_team')
router.register('v2/access/organization/(?P<organization_id>[0-9]+)/team/(?P<team_id>[0-9]+)/user', team_user_v2.ViewSet, basename='_api_v2_organization_team_user')

router.register('v2/assistance', assistance_index_v2.Index, basename='_api_v2_assistance_home')
router.register('v2/assistance/knowledge_base', knowledge_base_v2.ViewSet, basename='_api_v2_knowledge_base')

router.register('v2/base', base_index_v2.Index, basename='_api_v2_base_home')
router.register('v2/base/content_type', content_type_v2.ViewSet, basename='_api_v2_content_type')
router.register('v2/base/permission', permission_v2.ViewSet, basename='_api_v2_permission')
router.register('v2/base/user', user_v2.ViewSet, basename='_api_v2_user')

router.register('v2/config_management', config_management_v2.Index, basename='_api_v2_config_management_home')
router.register('v2/config_management/group', config_group_v2.ViewSet, basename='_api_v2_config_group')
router.register('v2/config_management/group/(?P<parent_group>[0-9]+)/child_group', config_group_v2.ViewSet, basename='_api_v2_config_group_child')
router.register('v2/config_management/group/(?P<group_id>[0-9]+)/software', config_group_software_v2.ViewSet, basename='_api_v2_config_group_software')

router.register('v2/itam', itam_index_v2.Index, basename='_api_v2_itam_home')

router.register('v2/itim', itim_v2.Index, basename='_api_v2_itim_home')

router.register('v2/project_management', project_management_v2.Index, basename='_api_v2_project_management_home')

router.register('v2/settings', settings_index_v2.Index, basename='_api_v2_settings_home')
router.register('v2/settings/knowledge_base_category', knowledge_base_category_v2.ViewSet, basename='_api_v2_knowledge_base_category')

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

from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework.routers import DefaultRouter

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
    knowledge_base_category as knowledge_base_category_v2,
)

from config_management.viewsets import (
    index as config_management_v2,
    config_group as config_group_v2,
    config_group_software as config_group_software_v2
)

from core.viewsets import (
    history as history_v2,
    notes as notes_v2,
    manufacturer as manufacturer_v2,
    celery_log as celery_log_v2
)

from itam.viewsets import (
    index as itam_index_v2,
    device as device_v2,
    device_model as device_model_v2,
    device_type as device_type_v2,
    device_software as device_software_v2,
    operating_system as operating_system_v2,
    operating_system_version as operating_system_version_v2,
    software as software_v2,
    software_category as software_category_v2,
    software_version as software_version_v2,
)

from itim.viewsets import (
    index as itim_v2,
    cluster as cluster_v2,
    cluster_type as cluster_type_v2,
    port as port_v2,
    service as service_v2,
    service_device as service_device_v2
)

from project_management.viewsets import (
    index as project_management_v2,
    project as project_v2,
    project_milestone as project_milestone_v2,
    project_state as project_state_v2,
    project_type as project_type_v2,
)

from settings.viewsets import (
    app_settings as app_settings_v2,
    external_link as external_link_v2,
    index as settings_index_v2,
    user_settings as user_settings_v2
)

app_name = "API"


router = DefaultRouter(trailing_slash=False)


router.register('', v2.Index, basename='_api_v2_home')

router.register('access', access_v2.Index, basename='_api_v2_access_home')
router.register('access/organization', organization_v2.ViewSet, basename='_api_v2_organization')
router.register('access/organization/(?P<organization_id>[0-9]+)/team', team_v2.ViewSet, basename='_api_v2_organization_team')
router.register('access/organization/(?P<organization_id>[0-9]+)/team/(?P<team_id>[0-9]+)/user', team_user_v2.ViewSet, basename='_api_v2_organization_team_user')


router.register('assistance', assistance_index_v2.Index, basename='_api_v2_assistance_home')
router.register('assistance/knowledge_base', knowledge_base_v2.ViewSet, basename='_api_v2_knowledge_base')


router.register('base', base_index_v2.Index, basename='_api_v2_base_home')
router.register('base/content_type', content_type_v2.ViewSet, basename='_api_v2_content_type')
router.register('base/permission', permission_v2.ViewSet, basename='_api_v2_permission')
router.register('base/user', user_v2.ViewSet, basename='_api_v2_user')


router.register('config_management', config_management_v2.Index, basename='_api_v2_config_management_home')
router.register('config_management/group', config_group_v2.ViewSet, basename='_api_v2_config_group')
router.register('config_management/group/(?P<parent_group>[0-9]+)/child_group', config_group_v2.ViewSet, basename='_api_v2_config_group_child')
router.register('config_management/group/(?P<group_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_config_group_notes')
router.register('config_management/group/(?P<group_id>[0-9]+)/software', config_group_software_v2.ViewSet, basename='_api_v2_config_group_software')


router.register('core/(?P<model_class>.+)/(?P<model_id>[0-9]+)/history', history_v2.ViewSet, basename='_api_v2_model_history')


router.register('itam', itam_index_v2.Index, basename='_api_v2_itam_home')
router.register('itam/device', device_v2.ViewSet, basename='_api_v2_device')
router.register('itam/device/(?P<device_id>[0-9]+)/software', device_software_v2.ViewSet, basename='_api_v2_device_software')
router.register('itam/device/(?P<device_id>[0-9]+)/service', service_device_v2.ViewSet, basename='_api_v2_service_device')
router.register('itam/device/(?P<device_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_device_notes')
router.register('itam/operating_system', operating_system_v2.ViewSet, basename='_api_v2_operating_system')
router.register('itam/operating_system/(?P<operating_system_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_operating_system_notes')
router.register('itam/operating_system/(?P<operating_system_id>[0-9]+)/version', operating_system_version_v2.ViewSet, basename='_api_v2_operating_system_version')
router.register('itam/software', software_v2.ViewSet, basename='_api_v2_software')
router.register('itam/software/(?P<software_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_software_notes')
router.register('itam/software/(?P<software_id>[0-9]+)/version', software_version_v2.ViewSet, basename='_api_v2_software_version')


router.register('itim', itim_v2.Index, basename='_api_v2_itim_home')
router.register('itim/cluster', cluster_v2.ViewSet, basename='_api_v2_cluster')
router.register('itim/cluster/(?P<cluster_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_cluster_notes')
router.register('itim/service', service_v2.ViewSet, basename='_api_v2_service')
router.register('itim/service/(?P<service_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_service_notes')


router.register('project_management', project_management_v2.Index, basename='_api_v2_project_management_home')
router.register('project_management/project', project_v2.ViewSet, basename='_api_v2_project')
router.register('project_management/project/(?P<project_id>[0-9]+)/milestone', project_milestone_v2.ViewSet, basename='_api_v2_project_milestone')
router.register('itim/project_management/project/(?P<project_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_project_notes')


router.register('settings', settings_index_v2.Index, basename='_api_v2_settings_home')
router.register('settings/app_settings', app_settings_v2.ViewSet, basename='_api_v2_app_settings')
router.register('settings/celery_log', celery_log_v2.ViewSet, basename='_api_v2_celery_log')
router.register('settings/cluster_type', cluster_type_v2.ViewSet, basename='_api_v2_cluster_type')
router.register('settings/cluster_type/(?P<cluster_type_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_cluster_type_notes')
router.register('settings/device_model', device_model_v2.ViewSet, basename='_api_v2_device_model')
router.register('settings/device_type', device_type_v2.ViewSet, basename='_api_v2_device_type')
router.register('settings/external_link', external_link_v2.ViewSet, basename='_api_v2_external_link')
router.register('settings/knowledge_base_category', knowledge_base_category_v2.ViewSet, basename='_api_v2_knowledge_base_category')
router.register('settings/manufacturer', manufacturer_v2.ViewSet, basename='_api_v2_manufacturer')
router.register('settings/manufacturer/(?P<manufacturer_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_manufacturer_notes')
router.register('settings/port', port_v2.ViewSet, basename='_api_v2_port')
router.register('settings/port/(?P<port_id>[0-9]+)/notes', notes_v2.ViewSet, basename='_api_v2_port_notes')
router.register('settings/project_state', project_state_v2.ViewSet, basename='_api_v2_project_state')
router.register('settings/project_type', project_type_v2.ViewSet, basename='_api_v2_project_type')
router.register('settings/software_category', software_category_v2.ViewSet, basename='_api_v2_software_category')
router.register('settings/user_settings', user_settings_v2.ViewSet, basename='_api_v2_user_settings')


urlpatterns = [

    path('schema', SpectacularAPIView.as_view(api_version='v2'), name='schema-v2',),
    path('docs', SpectacularSwaggerView.as_view(url_name='schema-v2'), name='_api_v2_docs'),

]

urlpatterns += router.urls

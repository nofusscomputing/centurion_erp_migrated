from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from itam.serializers.device import DeviceBaseSerializer

from project_management.models.projects import Project
from project_management.serializers.project_states import ProjectStateBaseSerializer



class ProjectBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_project-detail", format="html"
    )

    class Meta:

        model = Project

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]



class ProjectModelSerializer(ProjectBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_project-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'history': reverse(
                "API:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'milestone': reverse("API:_api_v2_project_milestone-list", request=self._context['view'].request, kwargs={'project_id': item.pk}),
            'notes': reverse("API:_api_v2_cluster_notes-list", request=self._context['view'].request, kwargs={'cluster_id': item.pk}),
            'tickets': 'ToDo'
        }


    class Meta:

        model = Project

        fields =  [
            'id',
            'external_ref',
            'external_system',
            'organization',
            'display_name',
            'name',
            'description',
            'priority',
            'state',
            'project_type',
            'code',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'manager_user',
            'manager_team',
            'team_members',
            'is_deleted',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



class ProjectViewSerializer(ProjectModelSerializer):

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    state = ProjectStateBaseSerializer( many = False, read_only = True )

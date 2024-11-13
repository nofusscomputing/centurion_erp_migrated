from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from itam.serializers.device import DeviceBaseSerializer

from app.serializers.user import UserBaseSerializer

from access.serializers.teams import TeamBaseSerializer

from core import fields as centurion_field

from project_management.models.projects import Project
from project_management.serializers.project_states import ProjectStateBaseSerializer
from project_management.serializers.project_type import ProjectTypeBaseSerializer



class ProjectBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_project-detail", format="html"
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

    def get_url(self, item) -> dict:

        return {
            '_self': reverse("v2:_api_v2_project-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'milestone': reverse("v2:_api_v2_project_milestone-list", request=self._context['view'].request, kwargs={'project_id': item.pk}),
            'notes': reverse("v2:_api_v2_project_notes-list", request=self._context['view'].request, kwargs={'project_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_ticket_project_task-list",
                request=self._context['view'].request,
                kwargs={
                    'project_id': item.pk
                }
            ),
        }

    description = centurion_field.MarkdownField( required = False, style_class = 'large' )

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
            'external_ref',
            'external_system',
            'created',
            'modified',
            '_urls',
        ]



class ProjectImportSerializer(ProjectModelSerializer):


    class Meta(ProjectModelSerializer.Meta):


        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



class ProjectViewSerializer(ProjectModelSerializer):

    manager_team = TeamBaseSerializer( many = False, read_only = True )

    manager_user = UserBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    state = ProjectStateBaseSerializer( many = False, read_only = True )

    team_members = UserBaseSerializer( many = True, read_only = True )

    project_type = ProjectTypeBaseSerializer( many = False, read_only = True )

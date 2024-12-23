from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from assistance.serializers.knowledge_base import KnowledgeBaseBaseSerializer

from project_management.models.project_states import ProjectState



class ProjectStateBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_project_state-detail", format="html"
    )


    class Meta:

        model = ProjectState

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



class ProjectStateModelSerializer(
    common.CommonModelSerializer,
    ProjectStateBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
        }


    class Meta:

        model = ProjectState

        fields =  [
            'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'runbook',
            'is_completed',
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



class ProjectStateViewSerializer(ProjectStateModelSerializer):

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    runbook = KnowledgeBaseBaseSerializer( many = False, read_only = True )

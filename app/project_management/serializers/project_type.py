from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from assistance.serializers.knowledge_base import KnowledgeBaseBaseSerializer

from project_management.models.project_types import ProjectType



class ProjectTypeBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_project_type-detail", format="html"
    )


    class Meta:

        model = ProjectType

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


class ProjectTypeModelSerializer(ProjectTypeBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse(
                "API:_api_v2_project_type-detail",
                request=self._context['view'].request,
                kwargs={
                    'pk': item.pk
                }
            ),
        }


    class Meta:

        model = ProjectType

        fields =  [
            'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'runbook',
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



class ProjectTypeViewSerializer(ProjectTypeModelSerializer):

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    runbook = KnowledgeBaseBaseSerializer( many = False, read_only = True )

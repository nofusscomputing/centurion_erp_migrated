from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from project_management.models.project_milestone import ProjectMilestone
from project_management.serializers.project import Project, ProjectBaseSerializer



class ProjectMilestoneBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url =  serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        context = self.context.copy()

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = ProjectMilestone

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


class ProjectMilestoneModelSerializer(
    common.CommonModelSerializer,
    ProjectMilestoneBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
        }


    class Meta:

        model = ProjectMilestone

        fields =  [
            'id',
            'organization',
            'display_name',
            'name',
            'description',
            'start_date',
            'finish_date',
            'project',
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


    def __init__(self, instance=None, data=empty, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)

        self.fields.fields['project'].read_only = True

        self.fields.fields['organization'].read_only = True


    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)

        project = Project.objects.get(
                pk = int(self._kwargs['context']['view'].kwargs['project_id'])
            )

        self.validated_data.update({
            'organization': project.organization,
            'project': project
        })

        return is_valid



class ProjectMilestoneViewSerializer(ProjectMilestoneModelSerializer):

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    project = ProjectBaseSerializer( many = False, read_only = True )

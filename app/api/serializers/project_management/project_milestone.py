from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from project_management.models.projects import Project
from project_management.models.project_milestone import ProjectMilestone



class ProjectMilestoneSerializer(
    serializers.ModelSerializer,
):

    url = serializers.SerializerMethodField('get_url_project_milestone')

    def get_url_project_milestone(self, item):

        request = self.context.get('request')

        return request.build_absolute_uri(
            reverse('v1:_api_project_milestone-detail',
                kwargs={
                    'project_id': item.project.id,
                    'pk': item.id
                }
            )
        )


    class Meta:

        model = ProjectMilestone

        fields = [
            'name',
            'description',
            'organization',
            'project',
            'start_date',
            'finish_date',
            'created',
            'modified',
            'url',
        ]

        read_only_fields = [
            'id',
            'url',
        ]


    def __init__(self, instance=None, data=empty, **kwargs):

        self.fields.fields['organization'].read_only = True
        self.fields.fields['project'].read_only = True

        super().__init__(instance=instance, data=data, **kwargs)


    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)

        project = Project.objects.get(
                pk = int(self._kwargs['context']['view'].kwargs['project_id'])
            )

        self._validated_data.update({
            'organization': project.organization,
            'project': project
        })

        return is_valid

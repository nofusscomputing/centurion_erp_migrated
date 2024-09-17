from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from project_management.models.projects import Project



class ProjectSerializer(
    serializers.ModelSerializer,
):

    url = serializers.SerializerMethodField('get_url')


    def get_url(self, item):

        request = self.context.get('request')

        return request.build_absolute_uri(reverse("API:_api_projects-detail", args=[item.pk]))


    project_tasks_url = serializers.SerializerMethodField('get_url_project_tasks')


    def get_url_project_tasks(self, item):

        request = self.context.get('request')

        return request.build_absolute_uri(
            reverse(
                'API:_api_project_tasks-list',
                kwargs={
                    'project_id': item.id
                }
            )
        )

    class Meta:

        model = Project

        fields =  [
            'id',
            'organization',
            'state',
            'project_type',
            'priority',
            'name',
            'description',
            'code',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'manager_user',
            'manager_team',
            'team_members',
            'project_tasks_url',
            'created',
            'modified',
            'external_ref',
            'external_system',
            'url',
        ]

        read_only_fields = [
            'id',
            'url',
        ]

from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from project_management.models.projects import Project



class ProjectSerializer(
    serializers.ModelSerializer,
):

    percent_completed = serializers.CharField(
        read_only = True,        
    )

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


    project_milestone_url = serializers.SerializerMethodField('get_url_project_milestone')

    def get_url_project_milestone(self, item):

        request = self.context.get('request')

        return request.build_absolute_uri(
            reverse(
                'API:_api_project_milestone-list',
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
            'project_milestone_url',
            'percent_completed',
            'created',
            'modified',
            'url',
        ]

        read_only_fields = [
            'id',
            'url',
            'created',
            'modified',
        ]



class ProjectImportSerializer(ProjectSerializer):

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
            'project_milestone_url',
            'percent_completed',
            'created',
            'modified',
            'external_ref',
            'external_system',
            'is_deleted',
            'url',
        ]

        read_only_fields = [
            'id',
            'url',
        ]

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


    class Meta:

        model = Project

        fields =  [
            'id',
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
            'created',
            'modified',
            'url',
        ]

        read_only_fields = [
            'id',
            'url',
        ]

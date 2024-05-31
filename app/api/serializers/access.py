from rest_framework import serializers, request
from rest_framework.reverse import reverse
from access.models import Organization, Team

from django.contrib.auth.models import Permission



class TeamSerializerBase(serializers.ModelSerializer):

    view_name="_api_team"

    url = serializers.SerializerMethodField('get_url')


    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            'organization',
            'url',
        )


    def get_url(self, obj):

        request = self.context.get('request')

        return request.build_absolute_uri(reverse(self.view_name, args=[obj.organization.id,obj.pk]))



class TeamSerializer(TeamSerializerBase):

    permissions = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):

        request = self.context.get('request')

        team = Team.objects.get(pk=obj.id)

        return request.build_absolute_uri(reverse('_api_team_permission', args=[team.organization_id,team.id]))


    class Meta:
        model = Team
        depth = 1
        fields = (
            "id",
            "team_name",
            'organization',
            'permissions',
            'url',
        )
        read_only_fields = [
            'permissions'
        ]



class OrganizationSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="_api_organization", format="html"
    )

    teams = TeamSerializerBase(source='team_set', many=True, read_only=False)

    view_name="_api_organization"


    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            'teams',
            'url',
        )

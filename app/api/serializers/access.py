from rest_framework import serializers, request
from rest_framework.reverse import reverse
from access.models import Organization, Team

from django.contrib.auth.models import Permission



class TeamSerializerBase(serializers.ModelSerializer):

    url = serializers.SerializerMethodField('get_url')


    class Meta:
        model = Team
        fields = (
            "id",
            "team_name",
            'organization',
            'url',
        )


    def get_url(self, obj):

        request = self.context.get('request')

        return request.build_absolute_uri(reverse("API:_api_team", args=[obj.organization.id,obj.pk]))



class TeamSerializer(TeamSerializerBase):

    permissions = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):

        request = self.context.get('request')

        team = Team.objects.get(pk=obj.id)

        return request.build_absolute_uri(reverse('API:_api_team_permission', args=[team.organization_id,team.id]))


    url = serializers.SerializerMethodField('team_url')

    def team_url(self, obj):

        request = self.context.get('request')

        return request.build_absolute_uri(reverse('API:_api_team', args=[obj.organization_id,obj.id]))


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



class OrganizationListSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_organization", format="html"
    )


    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            'url',
        )



class OrganizationSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_organization", format="html"
    )

    teams = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):

        request = self.context.get('request')

        team = Team.objects.get(pk=obj.id)

        return request.build_absolute_uri(reverse('API:_api_organization_teams', args=[team.organization_id]))

    view_name="API:_api_organization"


    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            'teams',
            'url',
        )

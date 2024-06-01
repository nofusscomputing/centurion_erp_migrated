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


    def validate(self, data):
        """
        Check that start is before finish.
        """

        data['organization_id'] = self._context['view'].kwargs['organization_id']

        return data


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
            'permissions',
            'url'
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

    team_url = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):

        request = self.context.get('request')

        team = Team.objects.filter(pk=obj.id)

        return request.build_absolute_uri(reverse('API:_api_organization_teams', args=[obj.id]))

    teams = TeamSerializerBase(source='team_set', many=True, read_only=False)

    view_name="API:_api_organization"


    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            'teams',
            'url',
            'team_url',
        )

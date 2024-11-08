from rest_framework.reverse import reverse

from rest_framework import serializers

from access.models import Team
from access.serializers.organization import OrganizationBaseSerializer

from app.serializers.permission import PermissionBaseSerializer



class TeamBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return reverse(
            "v2:_api_v2_organization_team-detail",
            request=self.context['view'].request,
            kwargs={
                'organization_id': item.organization.id,
                'pk': item.pk
            }
        )


    class Meta:

        model = Team

        fields = [
            'id',
            'display_name',
            'team_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'team_name',
            'url',
        ]



class TeamModelSerializer(TeamBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': reverse(
                'v2:_api_v2_organization_team-detail',
                request=self.context['view'].request,
                kwargs={
                    'organization_id': item.organization.id,
                    'pk': item.pk
                }
            ),
            'users': reverse(
                'v2:_api_v2_organization_team_user-list',
                request=self.context['view'].request,
                kwargs={
                    'organization_id': item.organization.id,
                    'team_id': item.pk
                }
            )
        }


    class Meta:

        model = Team

        fields = '__all__'

        fields =  [
             'id',
            'display_name',
            'team_name',
            'model_notes',
            'permissions',
            'organization',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'organization',
            'created',
            'modified',
            '_urls',
        ]



    def is_valid(self, *, raise_exception=True) -> bool:

        is_valid = False

        is_valid = super().is_valid(raise_exception=raise_exception)

        self.validated_data['organization_id'] = int(self._context['view'].kwargs['organization_id'])


        return is_valid



class TeamViewSerializer(TeamModelSerializer):

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    permissions = PermissionBaseSerializer(many = True)

from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from access.models import TeamUsers
from app.serializers.user import UserBaseSerializer



class TeamUserBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return reverse(
            "API:_api_v2_organization_team_user-detail",
            request=self.context['view'].request,
            kwargs={
                'organization_id': item.team.organization.id,
                'team_id': item.team.id,
                'pk': item.pk
            }
        )


    class Meta:

        model = TeamUsers

        fields = [
            'id',
            'display_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url',
        ]



class TeamUserModelSerializer(TeamUserBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse(
                'API:_api_v2_organization_team_user-detail',
                request=self.context['view'].request,
                kwargs={
                    'organization_id': item.team.organization.id,
                    'team_id': item.team.id,
                    'pk': item.pk
                }
            )
        }


    class Meta:

        model = TeamUsers

        fields =  [
             'id',
            'display_name',
            'manager',
            'user',
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



    def is_valid(self, *, raise_exception=True) -> bool:

        is_valid = False

        try:

            is_valid = super().is_valid(raise_exception=raise_exception)

            self.validated_data['team_id'] = int(self._context['view'].kwargs['team_id'])

        except Exception as unhandled_exception:

            ParseError( 
                detail=f"Server encountered an error during validation, Traceback: {unhandled_exception.with_traceback}"
            )

        return is_valid



class TeamUserViewSerializer(TeamUserModelSerializer):

    user = UserBaseSerializer(read_only = True)

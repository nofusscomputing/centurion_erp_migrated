from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from access.serializers.organization import OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from app.serializers.user import UserBaseSerializer

from assistance.models.knowledge_base import KnowledgeBase
from assistance.serializers.knowledge_base_category import KnowledgeBaseCategoryBaseSerializer


class KnowledgeBaseBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return reverse(
            "API:_api_v2_knowledge_base-detail",
            request=self.context['view'].request,
            kwargs={
                'pk': item.pk
            }
        )


    class Meta:

        model = KnowledgeBase

        fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]



class KnowledgeBaseModelSerializer(KnowledgeBaseBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse(
                'API:_api_v2_knowledge_base-detail',
                request=self.context['view'].request,
                kwargs={
                    'pk': item.pk
                }
            ),
            'category': reverse(
                'API:_api_v2_knowledge_base_category-list',
                request=self.context['view'].request,
            ),
            'organization': reverse(
                'API:_api_v2_organization-list',
                request=self.context['view'].request,
            ),
            'team': reverse(
                'API:_api_v2_organization_team-list',
                request=self.context['view'].request,
                kwargs={
                    'organization_id': item.organization.id,
                }
            ),
            'user': reverse(
                'API:_api_v2_user-list',
                request=self.context['view'].request,
            )
        }


    class Meta:

        model = KnowledgeBase

        fields =  [
            'id',
            'organization',
            'category',
            'display_name',
            'title',
            'summary',
            'content',
            'release_date',
            'expiry_date',
            'target_user',
            'target_team',
            'responsible_user',
            'responsible_teams',
            'public',
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



    def is_valid(self, *, raise_exception=True) -> bool:

        is_valid = False

        is_valid = super().is_valid(raise_exception=raise_exception)

        target_team = None
        target_user = None


        if self.instance:

            if len(self.instance.target_team.filter()) > 0:

                target_team = self.instance.target_team.filter()[0]


            if hasattr(self.instance, 'target_user_id'):

                target_user = self.instance.target_user_id


        if 'target_team' in self.validated_data:

            target_team = self.validated_data['target_team']


        if 'target_user' in self.validated_data:

            target_user = self.validated_data['target_user']


        if target_team and target_user:

            is_valid = False

            raise ValidationError('Both a Target Team or Target User Cant be assigned at the same time. Use one or the other')


        if not target_team and not target_user:

            raise ValidationError('A Target Team or Target User must be assigned.')


        return is_valid



class KnowledgeBaseViewSerializer(KnowledgeBaseModelSerializer):

    category = KnowledgeBaseCategoryBaseSerializer( read_only = True )

    organization = OrganizationBaseSerializer( many=False, read_only=True )

    responsible_teams = TeamBaseSerializer( read_only = True, many = True)

    responsible_user = UserBaseSerializer( read_only = True )

    target_team = TeamBaseSerializer( read_only = True, many = True)

    target_user = UserBaseSerializer( read_only = True )

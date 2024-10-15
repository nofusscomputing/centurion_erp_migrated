from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError


from access.serializers.organization import OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from app.serializers.user import UserBaseSerializer

from assistance.models.knowledge_base import KnowledgeBaseCategory



class KnowledgeBaseCategoryBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return reverse(
            "API:_api_v2_knowledge_base_category-detail",
            request=self.context['view'].request,
            kwargs={
                'pk': item.pk
            }
        )


    class Meta:

        model = KnowledgeBaseCategory

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]



class KnowledgeBaseCategoryModelSerializer(KnowledgeBaseCategoryBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse(
                'API:_api_v2_knowledge_base_category-detail',
                request=self.context['view'].request,
                kwargs={
                    'pk': item.pk
                }
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

        model = KnowledgeBaseCategory

        fields = '__all__'

        fields =  [
            'id',
            'organization',
            'name',
            'parent_category',
            'target_user',
            'target_team',
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


        if self.validated_data['target_team'] and self.validated_data['target_user']:

            is_valid = False

            raise ValidationError('Both a Target Team or Target User Cant be assigned at the same time. Use one or the other or None')


        return is_valid



class KnowledgeBaseCategoryViewSerializer(KnowledgeBaseCategoryModelSerializer):

    organization = OrganizationBaseSerializer( many=False, read_only=True )\
    
    parent_category = KnowledgeBaseCategoryBaseSerializer( many = False, read_only = True)

    target_team = TeamBaseSerializer( read_only = True, many = True)

    target_user = UserBaseSerializer( read_only = True )

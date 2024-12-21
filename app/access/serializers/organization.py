from rest_framework.reverse import reverse

from rest_framework import serializers

from access.models import Organization

from app.serializers.user import UserBaseSerializer

from core import fields as centurion_field



class OrganizationBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_organization-detail", format="html"
    )

    class Meta:

        model = Organization

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



class OrganizationModelSerializer(
    OrganizationBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
            'teams': reverse("v2:_api_v2_organization_team-list", request=self._context['view'].request, kwargs={'organization_id': item.pk}),
        }

    model_notes = centurion_field.MarkdownField( required = False )

    class Meta:

        model = Organization

        fields = '__all__'

        fields =  [
             'id',
            'display_name',
            'name',
            'model_notes',
            'manager',
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


class OrganizationViewSerializer(OrganizationModelSerializer):
    pass

    manager = UserBaseSerializer(many=False, read_only = True)

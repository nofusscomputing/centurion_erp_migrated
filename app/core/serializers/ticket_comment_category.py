from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from app.serializers.user import UserBaseSerializer

from core.models.ticket.ticket_comment_category import TicketCommentCategory



class TicketCommentCategoryBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_ticket_comment_category-detail", format="html"
    )


    class Meta:

        model = TicketCommentCategory

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


class TicketCommentCategoryModelSerializer(TicketCommentCategoryBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("v2:_api_v2_ticket_comment_category-detail", 
                request=self._context['view'].request,
                kwargs={
                    'pk': item.pk
                }
            )
        }


    class Meta:

        model = TicketCommentCategory

        fields = '__all__'

        fields =  [
            'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
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



class TicketCommentCategoryViewSerializer(TicketCommentCategoryModelSerializer):

    organization = OrganizationBaseSerializer( read_only = True )

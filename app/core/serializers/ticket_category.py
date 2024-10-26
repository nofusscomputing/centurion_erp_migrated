from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from core.models.ticket.ticket_category import TicketCategory



class TicketCategoryBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_ticket_category-detail", format="html"
    )

    class Meta:

        model = TicketCategory

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


class TicketCategoryModelSerializer(TicketCategoryBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_ticket_category-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
        }


    class Meta:

        model = TicketCategory

        fields = '__all__'

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



class TicketCategoryViewSerializer(TicketCategoryModelSerializer):

    organization = OrganizationBaseSerializer(many=False, read_only=True)

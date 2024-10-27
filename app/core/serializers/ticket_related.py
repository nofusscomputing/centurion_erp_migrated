from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from core.serializers.ticket import TicketBaseSerializer

from core.models.ticket.ticket import RelatedTickets



class RelatedTicketBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        request = None

        ticket_id: int = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

            if 'ticket_id' in self._kwargs['context']['view'].kwargs:

                ticket_id = int(self._kwargs['context']['view'].kwargs['ticket_id'])

        return item.get_url( ticket_id = ticket_id,request = request )


    class Meta:

        model = RelatedTickets

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


class RelatedTicketModelSerializer(RelatedTicketBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        request = None

        ticket_id: int = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

            if 'ticket_id' in self._kwargs['context']['view'].kwargs:

                ticket_id = int(self._kwargs['context']['view'].kwargs['ticket_id'])

        return {
            '_self': item.get_url( ticket_id = ticket_id, request = request ),
        }


    class Meta:

        model = RelatedTickets

        fields =  [
             'id',
            'display_name',
            'to_ticket_id',
            'from_ticket_id',
            'how_related',
            'organization',
            '_urls',
        ]

        read_only_fields = [
             'id',
            'display_name',
            'to_ticket_id',
            'from_ticket_id',
            'how_related',
            'organization',
            '_urls',
        ]



class RelatedTicketViewSerializer(RelatedTicketModelSerializer):

    from_ticket_id = TicketBaseSerializer()

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    to_ticket_id = TicketBaseSerializer()

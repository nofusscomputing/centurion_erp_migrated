from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from core.serializers.ticket import Ticket, TicketBaseSerializer

from core import exceptions as centurion_exceptions
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
            '_urls',
        ]


    def validate(self, attrs):

        check_db = self.Meta.model.objects.filter(
            to_ticket_id = attrs['to_ticket_id'],
            from_ticket_id = attrs['from_ticket_id'],
        )

        check_db_inverse = self.Meta.model.objects.filter(
            to_ticket_id = attrs['from_ticket_id'],
            from_ticket_id = attrs['to_ticket_id'],
        )

        if check_db.count() > 0 or check_db_inverse.count() > 0:

            raise centurion_exceptions.ValidationError(
                detail = {
                    'to_ticket_id': f"Ticket is already related to #{attrs['to_ticket_id'].id}"
                },
                code = 'duplicate_entry'
            )

        return attrs


class RelatedTicketViewSerializer(RelatedTicketModelSerializer):

    from_ticket_id = TicketBaseSerializer()

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    to_ticket_id = TicketBaseSerializer()

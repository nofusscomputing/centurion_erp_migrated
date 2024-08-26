from django.urls import reverse

from rest_framework import serializers

from api.serializers.itim.ticket_comment import TicketCommentSerializer

from core.models.ticket.ticket import Ticket



class TicketSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_core_tickets-detail", format="html"
    )

    ticket_comments = serializers.SerializerMethodField('get_url_ticket_comments')


    def get_url_ticket_comments(self, item):

        request = self.context.get('request')
        return request.build_absolute_uri(reverse('API:_api_core_ticket_comments-list', args=[item.id]))


    class Meta:
        model = Ticket
        fields =  [
            'id',
            'assigned_teams',
            'assigned_users',
            'created',
            'modified',
            'status',
            'title',
            'description',
            'urgency',
            'impact',
            'priority',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'opened_by',
            'organization',
            'project',
            'subscribed_teams',
            'subscribed_users',
            'ticket_comments',
            'url',
        ]

        read_only_fields = [
            'id',
            'url',
        ]

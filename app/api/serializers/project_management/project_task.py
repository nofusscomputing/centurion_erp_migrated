from api.serializers.core.ticket import TicketSerializer

from core.models.ticket.ticket import Ticket



class ProjectTaskSerializer(
    TicketSerializer,
):

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
            'ticket_type',
            'url',
        ]

from rest_framework import serializers
from rest_framework.fields import empty

from app.serializers.user import UserBaseSerializer

from core.models.ticket.ticket_category import TicketCategory
from core.serializers.ticket import (
    Ticket,
    TicketBaseSerializer,
    TicketModelSerializer,
    TicketViewSerializer
)



class ChangeTicketBaseSerializer(
    TicketBaseSerializer
):

    class Meta( TicketBaseSerializer.Meta ):

        pass



class ChangeTicketModelSerializer(
    TicketModelSerializer,
    ChangeTicketBaseSerializer,
):


    category = serializers.PrimaryKeyRelatedField(
        queryset = TicketCategory.objects.filter(
            change = True
        ),
        required = False
    )

    status = serializers.ChoiceField(
        [(e.value, e.label) for e in Ticket.TicketStatus.Change],
        default = Ticket.TicketStatus.All.NEW,
        required = False,
    )


    class Meta( TicketModelSerializer.Meta ):

        fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'status_badge',
            'title',
            'description',
            'estimate',
            'duration',
            'urgency',
            'impact',
            'priority',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'opened_by',
            'organization',
            'project',
            'milestone',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'external_ref',
            'external_system',
            'status_badge',
            'ticket_type',
            '_urls',
        ]



class ChangeAddTicketModelSerializer(
    ChangeTicketModelSerializer,
):
    """Serializer for `Add` user

    Args:
        ChangeTicketModelSerializer (class): Model Serializer
    """


    category = serializers.PrimaryKeyRelatedField(
        read_only = True,
    )


    class Meta(ChangeTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'status_badge',
            'estimate',
            'duration',
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
            'project',
            'milestone',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]



class ChangeChangeTicketModelSerializer(
    ChangeTicketModelSerializer,
):
    """Serializer for `Change` user

    Args:
        ChangeTicketModelSerializer (class): Change Model Serializer
    """


    category = serializers.PrimaryKeyRelatedField(
        read_only = True,
    )

    status = serializers.ChoiceField(
        [(e.value, e.label) for e in Ticket.TicketStatus.Change],
        read_only = True,
    )


    class Meta(ChangeTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'status_badge',
            'estimate',
            'duration',
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
            'milestone',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]



class ChangeTriageTicketModelSerializer(
    ChangeTicketModelSerializer,
):
    """Serializer for `Triage` user

    Args:
        ChangeTicketModelSerializer (class): Change Model Serializer
    """


    class Meta(ChangeTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'created',
            'modified',
            'status_badge',
            'estimate',
            'duration',
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
            '_urls',
        ]



class ChangeImportTicketModelSerializer(
    ChangeTicketModelSerializer,
):
    """Serializer for `Import` user

    Args:
        ChangeTicketModelSerializer (class): Change Model Serializer
    """

    class Meta(ChangeTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'display_name',
            'status_badge',
            'ticket_type',
            '_urls',
        ]



class ChangeTicketViewSerializer(
    TicketViewSerializer,
    ChangeTicketModelSerializer,
):

    pass

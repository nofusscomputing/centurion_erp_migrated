from rest_framework import serializers

from app.serializers.user import UserBaseSerializer

from core.models.ticket.ticket_category import TicketCategory
from core.serializers.ticket import (
    Ticket,
    TicketBaseSerializer,
    TicketModelSerializer,
    TicketViewSerializer
)



class RequestTicketBaseSerializer(
    TicketBaseSerializer
):

    class Meta( TicketBaseSerializer.Meta ):

        pass



class RequestTicketModelSerializer(
    TicketModelSerializer,
    RequestTicketBaseSerializer,
):


    category = serializers.PrimaryKeyRelatedField(
        queryset = TicketCategory.objects.filter(
            request = True
        ),
        required = False
    )

    status = serializers.ChoiceField([(e.value, e.label) for e in Ticket.TicketStatus.Request])

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



class RequestAddTicketModelSerializer(
    RequestTicketModelSerializer,
):
    """Serializer for `Add` user

    Args:
        RequestTicketModelSerializer (class): Model Serializer
    """


    class Meta(RequestTicketModelSerializer.Meta):

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



class RequestChangeTicketModelSerializer(
    RequestTicketModelSerializer,
):
    """Serializer for `Change` user

    Args:
        RequestTicketModelSerializer (class): Request Model Serializer
    """

    class Meta(RequestTicketModelSerializer.Meta):

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



class RequestTriageTicketModelSerializer(
    RequestTicketModelSerializer,
):
    """Serializer for `Triage` user

    Args:
        RequestTicketModelSerializer (class): Request Model Serializer
    """


    class Meta(RequestTicketModelSerializer.Meta):

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
            'organization',
            '_urls',
        ]



class RequestImportTicketModelSerializer(
    RequestTicketModelSerializer,
):
    """Serializer for `Import` user

    Args:
        RequestTicketModelSerializer (class): Request Model Serializer
    """

    class Meta(RequestTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'display_name',
            'status_badge',
            'ticket_type',
            '_urls',
        ]



class RequestTicketViewSerializer(
    TicketViewSerializer,
    RequestTicketModelSerializer,
):

    pass

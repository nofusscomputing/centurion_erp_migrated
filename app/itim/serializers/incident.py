from rest_framework import serializers

from app.serializers.user import UserBaseSerializer

from core.serializers.ticket import (
    Ticket,
    TicketBaseSerializer,
    TicketModelSerializer,
    TicketViewSerializer
)



class IncidentTicketBaseSerializer(
    TicketBaseSerializer
):

    class Meta( TicketBaseSerializer.Meta ):

        pass



class IncidentTicketModelSerializer(
    IncidentTicketBaseSerializer,
    TicketModelSerializer,
):

    status = serializers.ChoiceField([(e.value, e.label) for e in Ticket.TicketStatus.Incident])

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



class IncidentAddTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Add` user

    Args:
        IncidentTicketModelSerializer (class): Model Serializer
    """


    class Meta(IncidentTicketModelSerializer.Meta):

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



class IncidentChangeTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Incident` user

    Args:
        IncidentTicketModelSerializer (class): Incident Model Serializer
    """

    class Meta(IncidentTicketModelSerializer.Meta):

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



class IncidentTriageTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Triage` user

    Args:
        IncidentTicketModelSerializer (class): Incident Model Serializer
    """


    class Meta(IncidentTicketModelSerializer.Meta):

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



class IncidentImportTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Import` user

    Args:
        IncidentTicketModelSerializer (class): Incident Model Serializer
    """

    class Meta(IncidentTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'display_name',
            'status_badge',
            'ticket_type',
            '_urls',
        ]



class IncidentTicketViewSerializer(
    IncidentTicketModelSerializer,
    TicketViewSerializer,
):

    pass

from rest_framework import serializers

from app.serializers.user import UserBaseSerializer

from core.models.ticket.ticket_category import TicketCategory
from core.serializers.ticket import (
    Ticket,
    TicketBaseSerializer,
    TicketModelSerializer,
    TicketViewSerializer
)



class ProjectTaskTicketBaseSerializer(
    TicketBaseSerializer
):

    class Meta( TicketBaseSerializer.Meta ):

        pass



class ProjectTaskTicketModelSerializer(
    TicketModelSerializer,
):


    category = serializers.PrimaryKeyRelatedField(
        queryset = TicketCategory.objects.filter(
            project_task = True
        ),
        required = False
    )

    status = serializers.ChoiceField([(e.value, e.label) for e in Ticket.TicketStatus.ProjectTask])


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



class ProjectTaskAddTicketModelSerializer(
    ProjectTaskTicketModelSerializer,
):
    """Serializer for `Add` user

    Args:
        ProjectTaskTicketModelSerializer (class): Model Serializer
    """


    class Meta(ProjectTaskTicketModelSerializer.Meta):

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
            'milestone',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]



class ProjectTaskChangeTicketModelSerializer(
    ProjectTaskTicketModelSerializer,
):
    """Serializer for `ProjectTask` user

    Args:
        ProjectTaskTicketModelSerializer (class): ProjectTask Model Serializer
    """

    class Meta(ProjectTaskTicketModelSerializer.Meta):

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



class ProjectTaskTriageTicketModelSerializer(
    ProjectTaskTicketModelSerializer,
):
    """Serializer for `Triage` user

    Args:
        ProjectTaskTicketModelSerializer (class): ProjectTask Model Serializer
    """


    class Meta(ProjectTaskTicketModelSerializer.Meta):

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



class ProjectTaskImportTicketModelSerializer(
    ProjectTaskTicketModelSerializer,
):
    """Serializer for `Import` user

    Args:
        ProjectTaskTicketModelSerializer (class): ProjectTask Model Serializer
    """

    class Meta(ProjectTaskTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'display_name',
            'status_badge',
            'ticket_type',
            '_urls',
        ]



class ProjectTaskTicketViewSerializer(
    TicketViewSerializer,
    ProjectTaskTicketModelSerializer,
):

    pass

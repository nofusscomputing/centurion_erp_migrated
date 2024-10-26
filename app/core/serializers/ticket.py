from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from app.serializers.user import UserBaseSerializer

from core.models.ticket.ticket import Ticket

from core.fields.badge import Badge, BadgeField



class TicketBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item):

        context = self.context.copy()

        return reverse(
            "v2:_api_v2_ticket_" + str(item.get_ticket_type_display()).lower() + "-detail",
            request=context['view'].request,
            kwargs={
                'pk': item.pk
            }
        )


    class Meta:

        model = Ticket

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


class TicketModelSerializer(TicketBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        context = self.context.copy()

        return {
            '_self': reverse(
                "v2:_api_v2_ticket_" + str(item.get_ticket_type_display()).lower() + "-detail",
                request=context['view'].request,
                kwargs={
                    'pk': item.pk
                }
            ),
        }


    duration = serializers.IntegerField(source='duration_ticket', read_only=True)

    status_badge = BadgeField(label='Status')


    class Meta:
        """Ticket Model Base Meta

        This class specifically has only `id` in fields and all remaining fields
        as ready only so as to prevent using this serializer directly. The intent
        is that for each ticket type there is a seperate serializer for that ticket
        type.

        These serializers are for items that are common for ALL tickets.
        """

        model = Ticket

        fields = [
            'id',
            '_urls',
        ]

        read_only_fields = [
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


    def is_valid(self, *, raise_exception=False):

        is_valid: bool = False

        is_valid = super().is_valid(raise_exception=raise_exception)

        try:

            self.validated_data['ticket_type'] = self._context['view'].ticket_type_id

        except:

            is_valid = False


        return is_valid



class TicketViewSerializer(TicketModelSerializer):

    assigned_users = UserBaseSerializer(many=True, label='Assigned Users')

    assigned_teams = TeamBaseSerializer(many=True)

    opened_by = UserBaseSerializer()

    subscribed_users = UserBaseSerializer(many=True)

    subscribed_teams = TeamBaseSerializer(many=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

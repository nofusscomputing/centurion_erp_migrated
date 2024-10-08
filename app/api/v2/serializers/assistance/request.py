from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer
# from api.serializers.core.ticket import TicketSerializer

from api.v2.serializers.core.ticket_category import TicketCategoryBaseSerializer
from api.v2.serializers.core.ticket_linked_item import TicketLinkedItemBaseSerializer
from api.v2.serializers.base.user import UserBaseSerializer

from core.models.ticket.ticket import Ticket

from core.fields.badge import Badge, BadgeField




class TicketBaseSerializer(serializers.ModelSerializer):

    # display_name = serializers.SerializerMethodField('get_display_name')

    # def get_display_name(self, item):

    #     return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_ticket_request-detail", format="html"
    )

    class Meta:

        model = Ticket

        # fields = '__all__'
        fields = [
            'id',
            # 'display_name',
            'title',
            'url',
        ]

        # read_only_fields = [
        #     'id',
        #     # 'display_name',
        #     'title',
        #     # 'url',
        # ]


class TicketModelSerializer(TicketBaseSerializer):


    # operating_system = OperatingSystemModelSerializer(source='id', many=False, read_only=False)

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_ticket_request-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'comments': reverse("API:_api_v2_assistance_request_ticket_comments-list", request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
            'linked_items': reverse("API:_api_v2_ticket_linked_item-list", request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
            'related_tickets': reverse("API:_api_v2_related_ticket-list", request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
            # 'history': 'ToDo',
            # 'notes': 'ToDo',
            # 'services': 'ToDo',
            # 'software': reverse("API:_api_v2_device_software-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
            # 'tickets': 'ToDo'
        }

    # rendered_config = serializers.SerializerMethodField('get_rendered_config')
    # rendered_config = serializers.JSONField(source='get_configuration')


    # def get_rendered_config(self, item):

    #     return item.get_configuration(0)


    status_badge = BadgeField(label='Status')
    duration = serializers.IntegerField(source='duration_ticket', read_only=True)



    class Meta:

        model = Ticket

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
            # 'planned_start_date',
            # 'planned_finish_date',
            # 'real_start_date',
            # 'real_finish_date',
            'opened_by',
            'organization',
            'project',
            'milestone',
            'subscribed_teams',
            'subscribed_users',
            # 'ticket_comments',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'status_badge',
            # 'ticket_type',
            '_urls',
        ]



    def __init__(self, instance=None, data=empty, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)

        # self.fields.fields['category'].queryset = self.fields.fields['category'].queryset.filter(
        #     request = True
        # )




class TicketViewSerializer(TicketModelSerializer):

    # device_model = DeviceModelBaseSerializer(many=False, read_only=True)

    # device_type = DeviceTypeBaseSerializer(many=False, read_only=True)

    assigned_users = UserBaseSerializer(many=True, label='Assigned Users')

    assigned_teams = TeamBaseSerializer(many=True)

    category = TicketCategoryBaseSerializer()

    opened_by = UserBaseSerializer()

    subscribed_users = UserBaseSerializer(many=True)

    subscribed_teams = TeamBaseSerializer(many=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)











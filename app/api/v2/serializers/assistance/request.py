from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

# from api.serializers.core.ticket import TicketSerializer

from api.v2.serializers.core.ticket_category import TicketCategoryBaseSerializer
from api.v2.serializers.base.user import UserBaseSerializer

from core.models.ticket.ticket import Ticket





class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_ticket_request-detail", format="html"
    )

    class Meta:

        model = Ticket

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]


class ModelSerializer(BaseSerializer):


    # operating_system = OperatingSystemModelSerializer(source='id', many=False, read_only=False)

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_ticket_request-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
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

    assigned_users = UserBaseSerializer(many=True, label='Assigned Users')

    category = TicketCategoryBaseSerializer()

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
            'title',
            'description',
            'estimate',
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
            'ticket_type',
            '_urls',
        ]



    def __init__(self, instance=None, data=empty, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)

        # self.fields.fields['category'].queryset = self.fields.fields['category'].queryset.filter(
        #     request = True
        # )




class ViewSerializer(ModelSerializer):

    # device_model = DeviceModelBaseSerializer(many=False, read_only=True)

    # device_type = DeviceTypeBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)











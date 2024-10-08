from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
# from api.v2.serializers.itam.device_model import BaseSerializer as DeviceModelBaseSerializer
# from api.v2.serializers.itam.device_type import BaseSerializer as DeviceTypeBaseSerializer
# from api.v2.serializers.itam.operating_system import BaseSerializer as OperatingSystemModelSerializer

from api.v2.serializers.assistance.request import TicketBaseSerializer

from core.models.ticket.ticket import RelatedTickets



class RelatedTicketsBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device-detail", format="html"
    )

    # ticket_id = serializers.SerializerMethodField('get_ticket_id')

    # def get_ticket_id(self, item):

    #     related_ticket = RelatedTickets.object.get(id=int(item))

    #     if int(self._context['view'].kwargs['ticket_id']) == item.from_ticket_id_id:

    #         return 

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


class RelatedTicketsModelSerializer(RelatedTicketsBaseSerializer):


    # operating_system = OperatingSystemModelSerializer(source='id', many=False, read_only=False)

    # _urls = serializers.SerializerMethodField('get_url')

    # def get_url(self, item):

    #     return {
    #         '_self': '',
    #         # 'history': 'ToDo',
    #         # 'notes': 'ToDo',
    #         # 'services': 'ToDo',
    #         # 'software': reverse("API:_api_v2_device_software-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
    #         # 'tickets': 'ToDo'
    #     }

    # rendered_config = serializers.SerializerMethodField('get_rendered_config')
    # rendered_config = serializers.JSONField(source='get_configuration')


    # def get_rendered_config(self, item):

    #     return item.get_configuration(0)

    to_ticket_id = TicketBaseSerializer(label='To Ticket')


    from_ticket_id = TicketBaseSerializer(label='To Ticket')


    class Meta:

        model = RelatedTickets

        fields = '__all__'

        # fields =  [
        #      'id',
        #     'display_name',
        #     'name',
        #     'device_type',
        #     # 'operating_system',
        #     'model_notes',
        #     'serial_number',
        #     'uuid',
        #     'is_global',
        #     'is_virtual',
        #     'device_model',
        #     'config',
        #     'rendered_config',
        #     'inventorydate',
        #     'created',
        #     'modified',
        #     'organization',
        #     '_urls',
        # ]

        # read_only_fields = [
        #     'id',
        #     'display_name',
        #     # 'inventorydate',
        #     # 'created',
        #     # 'modified',
        #     # '_urls',
        # ]


    def __init__(self, instance=None, data=empty, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)

        # self.rendered_config = serializers.JSONField(initial=self.Meta.model.get_configuration(0))



class RelatedTicketsViewSerializer(RelatedTicketsModelSerializer):

    # device_model = DeviceModelBaseSerializer(many=False, read_only=True)

    # device_type = DeviceTypeBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

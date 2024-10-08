from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
# from api.v2.serializers.itam.device_model import BaseSerializer as DeviceModelBaseSerializer
# from api.v2.serializers.itam.device_type import BaseSerializer as DeviceTypeBaseSerializer
# from api.v2.serializers.itam.operating_system import BaseSerializer as OperatingSystemModelSerializer

from core.models.ticket.ticket_linked_items import TicketLinkedItem



class TicketLinkedItemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="API:_api_v2_device-detail", format="html"
    # )

    class Meta:

        model = TicketLinkedItem

        fields = [
            'id',
            'display_name',
            # 'name',
            # 'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            # 'name',
            # 'url',
        ]


class TicketLinkedItemModelSerializer(TicketLinkedItemBaseSerializer):


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


    class Meta:

        model = TicketLinkedItem

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



class TicketLinkedItemViewSerializer(TicketLinkedItemModelSerializer):

    # device_model = DeviceModelBaseSerializer(many=False, read_only=True)

    # device_type = DeviceTypeBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

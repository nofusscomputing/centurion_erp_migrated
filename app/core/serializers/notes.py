from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer


from core.models.notes import Notes



class NotesBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device-detail", format="html"
    )

    class Meta:

        model = Notes

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


class NotesModelSerializer(NotesBaseSerializer):


    # operating_system = OperatingSystemModelSerializer(source='id', many=False, read_only=False)

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_device_notes-detail", 
                request=self._context['view'].request,
                kwargs={'device_id': self._kwargs['context']['view'].kwargs['device_id'], 'pk': item.pk}
            ),
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


    class Meta:

        model = Notes

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

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]


    def __init__(self, instance=None, data=empty, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)

        # self.rendered_config = serializers.JSONField(initial=self.Meta.model.get_configuration(0))



class NotesViewSerializer(NotesModelSerializer):

    # device_model = DeviceModelBaseSerializer(many=False, read_only=True)

    # device_type = DeviceTypeBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

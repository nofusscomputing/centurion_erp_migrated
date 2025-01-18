from rest_framework.fields import empty
from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from itim.serializers.cluster import ClusterBaseSerializer
from itim.serializers.port import PortBaseSerializer
from itim.models.services import Service

from itam.serializers.device import Device, DeviceBaseSerializer



class ServiceBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_service-detail", format="html"
    )

    class Meta:

        model = Service

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


class ServiceModelSerializer(
    common.CommonModelSerializer,
    ServiceBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
            'external_links': reverse("v2:_api_v2_external_link-list", request=self._context['view'].request) + '?service=true',
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
            'notes': reverse("v2:_api_v2_service_notes-list", request=self._context['view'].request, kwargs={'service_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'service',
                    'item_id': item.pk
                    }
            )
        }


    rendered_config = serializers.JSONField( source='config_variables', read_only = True )


    class Meta:

        model = Service

        fields =  [
             'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'is_template',
            'template',
            'device',
            'cluster',
            'config',
            'rendered_config',
            'config_key_variable',
            'port',
            'dependent_service',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'rendered_config',
            'created',
            'modified',
            '_urls',
        ]


    def get_field_names(self, declared_fields, info):

        if 'view' in self._context:

            if 'device_id' in self._context['view'].kwargs:

                self.Meta.read_only_fields += [ 'cluster', 'device', 'organization', 'is_global' ]

        fields = super().get_field_names(declared_fields, info)

        return fields


    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)

        if 'view' in self._context:

            if 'device_id' in self._context['view'].kwargs:

                device = Device.objects.get( id = self._context['view'].kwargs['device_id'] )

                self.validated_data['device'] = device
                self.validated_data['organization'] = device.organization

        return is_valid


    def validate(self, attrs):

        attrs = super().validate(attrs=attrs)
        
        cluster = None

        config_key_variable = None

        device = None

        port = []

        port_required = False

        if self.instance:

            cluster = self.instance.cluster

            config_key_variable = self.instance.config_key_variable

            device = self.instance.device

            port = self.instance.port.all()


        if 'is_template' in attrs:

            is_template = attrs['is_template']

        else:

            is_template = self.fields.fields['is_template'].initial


        if 'template' in attrs:

            template = attrs['template']

        else:

            template = self.fields.fields['template'].initial


        if 'device' in attrs:

            device = attrs['device']


        if 'cluster' in attrs:

            cluster = attrs['cluster']

        
        if 'config_key_variable' in attrs:

            config_key_variable = attrs['config_key_variable']


        if 'port' in attrs:

            port = attrs['port']


        if not is_template and not template:

            if not device and not cluster:

                raise serializers.ValidationError(
                    detail = 'A Service must be assigned to either a "Cluster" or a "Device".',
                    code = 'one_of_cluster_or_device'
                )


            if device and cluster:

                raise serializers.ValidationError(
                    detail = 'A Service must only be assigned to either a "Cluster" or a "Device". Not both.',
                    code = 'either_cluster_or_device'
                )

            if len(port) == 0:

               port_required = True


        if template:

            if len(template.port.all()) == 0 and len(port) == 0:

                port_required = True


        if not is_template and not config_key_variable:

            raise serializers.ValidationError(
                detail = {
                    'config_key_variable': 'Configuration Key must be specified'
                },
                code = 'required'
            )

        if 'dependent_service' in attrs:

            if len(attrs['dependent_service']) > 0:

                for dependency in attrs['dependent_service']:

                    if hasattr(self.instance, 'pk'):

                        query = Service.objects.filter(
                            dependent_service = self.instance.pk,
                            id = dependency.id,
                        )

                        if query.exists():

                            raise serializers.ValidationError(
                                detail = {
                                    'dependent_service': 'A dependent service already depends upon this service. Circular dependencies are not allowed.'
                                },
                                code = 'no_circular_dependencies'
                            )

        if port_required:

             raise serializers.ValidationError(
                detail = {
                    'port': 'Port(s) must be assigned to a service.'
                },
                code = 'required'
            )

        return attrs



class ServiceViewSerializer(ServiceModelSerializer):

    cluster = ClusterBaseSerializer( many = False, read_only = True )

    device = DeviceBaseSerializer( many = False, read_only = True )

    dependent_service = ServiceBaseSerializer( many = True, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    port = PortBaseSerializer( many = True, read_only = True )

    template = ServiceBaseSerializer( many = False, read_only = True )

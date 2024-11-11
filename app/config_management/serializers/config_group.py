from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from config_management.models.groups import ConfigGroups

from itam.serializers.device import DeviceBaseSerializer

class ConfigGroupBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        request = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

        return item.get_url( request = request )


    class Meta:

        model = ConfigGroups

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



class ConfigGroupModelSerializer(
    common.CommonModelSerializer,
    ConfigGroupBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        request = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

        return {
            '_self': item.get_url( request = request ),
            'child_groups': reverse(
                'v2:_api_v2_config_group_child-list',
                request = self.context['view'].request,
                kwargs = {
                    'parent_group': item.pk
                }
            ),
            'configgroups': reverse(
                'v2:_api_v2_config_group-list',
                request = self.context['view'].request,
            ),
            'group_software': reverse(
                'v2:_api_v2_config_group_software-list',
                request=self.context['view'].request,
                kwargs = {
                    'group_id': item.pk
                }
            ),
            'notes': reverse(
                "v2:_api_v2_config_group_notes-list",
                request=self._context['view'].request,
                kwargs={'group_id': item.pk}
            ),
            'organization': reverse(
                'v2:_api_v2_organization-list',
                request=self.context['view'].request,
            ),
            'parent': reverse(
                'v2:_api_v2_config_group-list',
                request=self.context['view'].request,
            ),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'config_group',
                    'item_id': item.pk
                    }
            ),
        }

    rendered_config = serializers.JSONField( source = 'render_config', read_only=True )


    class Meta:

        model = ConfigGroups

        fields = [
            'id',
            'display_name',
            'organization',
            'parent',
            'name',
            'model_notes',
            'config',
            'hosts',
            'rendered_config',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]


    def get_field_names(self, declared_fields, info):

        fields = self.Meta.fields

        if 'view' in self._context:

            if 'parent_group' in self._context['view'].kwargs:

                self.Meta.read_only_fields += [ 
                    'organization',
                    'parent'
                ]

        return fields


    def is_valid(self, *, raise_exception=True) -> bool:

        is_valid = super().is_valid(raise_exception=raise_exception)

        if 'view' in self._context:

            if 'parent_group' in self._context['view'].kwargs:

                self.validated_data['parent_id'] = int(self._context['view'].kwargs['parent_group'])

                organization = self.Meta.model.objects.get(pk = int(self._context['view'].kwargs['parent_group']))

                self.validated_data['organization_id'] = organization.id

        return is_valid


    def validate(self, attrs):

        if self.instance:

            if hasattr(self.instance, 'parent_id') and 'parent' in self.initial_data:

                if self.initial_data['parent'] == self.instance.id:

                    raise serializers.ValidationError(
                        detail = {
                            'parent': 'Can not assign self as parent'
                        },
                        code = 'self_not_parent'
                    )

        return super().validate(attrs)



class ConfigGroupViewSerializer(ConfigGroupModelSerializer):

    hosts = DeviceBaseSerializer(read_only = True, many = True)

    parent = ConfigGroupBaseSerializer( read_only = True )

    organization = OrganizationBaseSerializer( many=False, read_only=True )

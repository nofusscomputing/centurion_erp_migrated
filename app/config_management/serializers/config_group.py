from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from app.serializers.user import UserBaseSerializer

from config_management.models.groups import ConfigGroups



class ConfigGroupBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return reverse(
            "API:_api_v2_config_group-detail",
            request=self.context['view'].request,
            kwargs={
                'pk': item.pk
            }
        )


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



class ConfigGroupModelSerializer(ConfigGroupBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse(
                'API:_api_v2_config_group-detail',
                request = self.context['view'].request,
                kwargs = {
                    'pk': item.pk
                }
            ),
            'configgroups': reverse(
                'API:_api_v2_config_group-list',
                request = self.context['view'].request,
            ),
            'organization': reverse(
                'API:_api_v2_organization-list',
                request=self.context['view'].request,
            ),
            'parent': reverse(
                'API:_api_v2_config_group-list',
                request=self.context['view'].request,
            ),
        }


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

    parent = ConfigGroupBaseSerializer( read_only = True )

    organization = OrganizationBaseSerializer( many=False, read_only=True )

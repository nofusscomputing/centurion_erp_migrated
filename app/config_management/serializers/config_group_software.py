from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from config_management.models.groups import ConfigGroupSoftware
from config_management.serializers.config_group import ConfigGroups, ConfigGroupBaseSerializer

from itam.serializers.software import SoftwareBaseSerializer
from itam.serializers.software_version import SoftwareVersion, SoftwareVersionBaseSerializer



class ConfigGroupSoftwareBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return reverse(
            "v2:_api_v2_config_group-detail",
            request=self.context['view'].request,
            kwargs={
                'group_id': item.config_group.pk,
                'pk': item.pk
            }
        )


    class Meta:

        model = ConfigGroupSoftware

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



class ConfigGroupSoftwareModelSerializer(ConfigGroupSoftwareBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': reverse(
                'v2:_api_v2_config_group_software-detail',
                request = self.context['view'].request,
                kwargs = {
                    'group_id': item.config_group.pk,
                    'pk': item.pk
                }
            ),
            'organization': reverse(
                'v2:_api_v2_organization-list',
                request=self.context['view'].request,
            ),
            'softwareversion': 'ToDo',
        }


    class Meta:

        model = ConfigGroupSoftware

        fields = '__all__'

        fields = [
            'id',
            'display_name',
            'organization',
            'config_group',
            'software',
            'action',
            'version',
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

            if 'group_id' in self._context['view'].kwargs:

                self.Meta.read_only_fields += [ 
                    'organization',
                    'config_group'
                ]

        return fields


    def is_valid(self, *, raise_exception=False) -> bool:

        is_valid = super().is_valid(raise_exception=raise_exception)

        if 'view' in self._context:

            if 'group_id' in self._context['view'].kwargs:

                self.validated_data['config_group_id'] = int(self._context['view'].kwargs['group_id'])

                parent_item = ConfigGroups.objects.get(pk = int(self._context['view'].kwargs['group_id']))

                self.validated_data['organization_id'] = parent_item.organization.id

        return is_valid


    def validate(self, attrs):

        if 'software' in self.initial_data:

            try:

                try:

                    current_object = self.Meta.model.objects.get( software_id = self.initial_data['software'] )

                except self.Meta.model.MultipleObjectsReturned:

                    pass    # Although an exception, the item still exists

                raise serializers.ValidationError(
                        detail = {
                            'software': 'This software is already assigned to this group'
                        },
                        code = 'software_exists'
                    )

            except self.Meta.model.DoesNotExist as exc:

                pass

        
        if 'version' in self.initial_data:

            if self.initial_data['version']:

                try:

                    current_object = SoftwareVersion.objects.get( pk = self.initial_data['version'] )


                    if 'software' in self.initial_data:

                        software = int(self.initial_data['software'])

                    elif self.instance:

                        software = self.instance.software


                    if software != current_object.software.id:

                        raise serializers.ValidationError(
                                detail = {
                                    'version': 'This version does not belong to selected software'
                                },
                                code = 'software_not_own_version'
                            )

                except self.Meta.model.DoesNotExist as exc:

                    raise serializers.ValidationError(
                            detail = {
                                'version': 'Software version does not exist'
                            },
                            code = 'version_absent'
                        )


        return super().validate(attrs)



class ConfigGroupSoftwareViewSerializer(ConfigGroupSoftwareModelSerializer):

    config_group = ConfigGroupBaseSerializer(read_only = True )

    organization = OrganizationBaseSerializer( many=False, read_only=True )

    software = SoftwareBaseSerializer( read_only = True )

    version = SoftwareVersionBaseSerializer( read_only = True )

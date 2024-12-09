
from rest_framework import serializers

from access.serializers.organization import Organization, OrganizationBaseSerializer

from core import fields as centurion_field

from settings.models.app_settings import AppSettings


class OrganizationField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        """ Queryset Override
        
        Override the base serializer and filter out the `global_organization`
        if defined.
        """

        app_settings = AppSettings.objects.all()

        queryset = Organization.objects.all()

        if getattr(app_settings[0], 'global_organization', None):

            queryset = queryset.exclude(id=app_settings[0].global_organization.id)

        return queryset



class CommonBaseSerializer(serializers.ModelSerializer):

    pass



class CommonModelSerializer(CommonBaseSerializer):
    """Common Model Serializer

    _**Note:** This serializer is not inherited by the organization Serializer_
    _`access.serializers.organization`, this is by design_

    This serializer is included within ALL model (Tenancy Model) serilaizers and is intended to be used
    to add objects that ALL model serializers will require.

    Args:
        CommonBaseSerializer (Class): Common base serializer
    """

    model_notes = centurion_field.MarkdownField( required = False )
    
    organization = OrganizationField(required = False)
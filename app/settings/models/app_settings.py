from django.db import models

from rest_framework.reverse import reverse

from access.fields import *
from access.models import Organization

from core.mixin.history_save import SaveHistory


class AppSettingsCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'Id of this setting',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    slug = None

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class AppSettings(AppSettingsCommonFields, SaveHistory):
    """ Application Settings

    This model is for storing settings for the application as a whole

    This class contains field `owner_organization` which exists so that in the future
    if there is a requirement for orgnizational settings, that this table can be used by
    specifying the `owner_organization`

    Raises:
        ValidationError: When software set as global and no organization has been specified 
    """

    class Meta:

        ordering = [
            'owner_organization'
        ]

        verbose_name = 'App Settings'

        verbose_name_plural = 'App Settings'


    owner_organization = models.ForeignKey(
        Organization,
        blank= True,
        help_text = 'Organization the settings belong to',
        default = None,
        null = True,
        on_delete=models.SET_DEFAULT,
        related_name = 'owner_organization'
    )

    device_model_is_global = models.BooleanField (
        blank= False,
        help_text = 'Should Device Models be global',
        default = False,
        verbose_name = 'Global Device Models',
    )

    device_type_is_global = models.BooleanField (
        blank= False,
        help_text = 'Should Device Types be global',
        default = False,
        verbose_name = 'Global Device Types',
    )

    manufacturer_is_global = models.BooleanField (
        blank= False,
        help_text = 'Should Manufacturers / Publishers be global',
        default = False,
        verbose_name = 'Global Manufacturers / Publishers',
    )

    software_is_global = models.BooleanField (
        blank= False,
        default = False,
        help_text = 'Should Software be global',
        verbose_name = 'Global Software',
    )

    software_categories_is_global = models.BooleanField (
        blank= False,
        default = False,
        help_text = 'Should Software be global',
        verbose_name = 'Global Software Categories',
    )

    global_organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_DEFAULT,
        blank= True,
        default = None,
        help_text = 'Organization global items will be created in',
        null = True,
        related_name = 'global_organization',
        verbose_name = 'Global Organization'
    )

    table_fields: list = []

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'global_organization',
                    ],
                    "right": [
                        'device_model_is_global',
                        'device_type_is_global',
                        'manufacturer_is_global',
                        'software_is_global',
                        'software_categories_is_global',

                    ]
                }
            ]
        }
    ]


    def get_organization(self):

        return self.global_organization



    def get_url( self, request = None ) -> str:

        model_name = str(self._meta.verbose_name.lower()).replace(' ', '_')


        if request:

            return reverse(f"v2:_api_v2_app_settings-detail", request=request, kwargs = { 'pk': self.pk } )

        return reverse(f"v2:_api_v2_app_settings-detail", kwargs = { 'pk': self.pk } )



    def clean(self):
        from django.core.exceptions import ValidationError

        if self.software_is_global and self.global_organization is None:

            raise ValidationError("Global Software must have a global organization")

    __all__ = [
        'device_model_is_global',
        'device_type_is_global',
        'manufacturer_is_global',
        'software_is_global',
        'software_categories_is_global',
        'global_organization',
    ]

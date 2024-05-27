from django.db import models

from access.fields import *
from access.models import Organization

from core.mixin.history_save import SaveHistory


class AppSettingsCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
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

    owner_organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        blank= True,
        default = None,
        null = True,
        help_text = 'Organization the settings belong to',
        related_name = 'owner_organization'
    )

    device_model_is_global = models.BooleanField (
        verbose_name = 'All Device Models are global',
        blank= False,
        default = False,
    )

    device_type_is_global = models.BooleanField (
        verbose_name = 'All Device Types is global',
        blank= False,
        default = False,
    )

    manufacturer_is_global = models.BooleanField (
        verbose_name = 'All Manufacturer / Publishers are global',
        blank= False,
        default = False,
    )

    software_is_global = models.BooleanField (
        verbose_name = 'All Software is global',
        blank= False,
        default = False,
    )

    software_categories_is_global = models.BooleanField (
        verbose_name = 'All Software Categories are global',
        blank= False,
        default = False,
    )

    global_organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_DEFAULT,
        blank= True,
        default = None,
        null = True,
        help_text = 'Organization global items will be created in',
        related_name = 'global_organization'
    )

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

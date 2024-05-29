from django.contrib.auth.models import User
from django.db import models

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory

from settings.models.app_settings import AppSettings

class ManufacturerCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()

    modified = AutoCreatedField()



class Manufacturer(TenancyObject, ManufacturerCommonFields, SaveHistory):


    class Meta:

        ordering = [
            'name'
        ]

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )


    slug = AutoSlugField()


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.manufacturer_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.manufacturer_is_global


    def __str__(self):

        return self.name

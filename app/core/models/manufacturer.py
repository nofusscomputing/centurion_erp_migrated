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
        blank=False,
        help_text = 'ID of manufacturer',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    created = AutoCreatedField()

    modified = AutoCreatedField()



class Manufacturer(TenancyObject, ManufacturerCommonFields, SaveHistory):


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Manufacturer'

        verbose_name_plural = 'Manufacturers'


    name = models.CharField(
        blank = False,
        help_text = 'Name of this manufacturer',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )


    slug = AutoSlugField()

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'name'
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]


    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified'
    ]


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.manufacturer_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.manufacturer_is_global


    def __str__(self):

        return self.name

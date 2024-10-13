from django.contrib.auth.models import User
from django.db import models

from itam.models.device_common import DeviceCommonFieldsName

from access.models import TenancyObject

from core.mixin.history_save import SaveHistory
from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings

class DeviceModel(DeviceCommonFieldsName, SaveHistory):


    class Meta:

        ordering = [
            'manufacturer',
            'name',
        ]

        verbose_name = 'Device Model'

        verbose_name_plural = 'Device Models'


    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'manufacturer',
                        'name',
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
        }
    ]

    table_fields: list = [
        'manufacturer',
        'name',
        'organization',
        'created',
        'modified'
    ]


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.device_model_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.device_model_is_global


    def __str__(self):

        return self.manufacturer.name + ' ' + self.name

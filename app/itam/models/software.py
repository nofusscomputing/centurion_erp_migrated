from django.db import models

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory
from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings


class SoftwareCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )

    slug = AutoSlugField()

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class SoftwareCategory(SoftwareCommonFields, SaveHistory):


    class Meta:

        verbose_name_plural = 'Software Categories'



    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_categories_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.software_categories_is_global


    def __str__(self):

        return self.name



class Software(SoftwareCommonFields, SaveHistory):


    class Meta:

        ordering = [
            'name',
            'publisher__name'
        ]

        verbose_name = 'Software'

        verbose_name_plural = 'Softwares'


    publisher = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )

    category = models.ForeignKey(
        SoftwareCategory,
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
                        'publisher',
                        'name',
                        'category',
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
            "name": "Versions",
            "slug": "version",
            "sections": [
                {
                    "layout": "table",
                    "field": "versions",
                }
            ]
        },
        # {
        #     "name": "Licences",
        #     "slug": "licence",
        #     "sections": [
        #         {
        #             "layout": "table",
        #             "field": "licences",
        #         }
        #     ],
        # },
        {
            "name": "Installations",
            "slug": "installs",
            "sections": [
                {
                    "layout": "table",
                    "field": "installations",
                }
            ],
        },
        {
            "name": "Tickets",
            "slug": "tickets",
            "sections": [
                {
                    "layout": "table",
                    "field": "tickets",
                }
            ],
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    ]

    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.software_is_global


    def __str__(self):

        return self.name



class SoftwareVersion(SoftwareCommonFields, SaveHistory):


    class Meta:

        verbose_name_plural = 'Software Versions'


    software = models.ForeignKey(
        Software,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = False,
    )


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.software


    def __str__(self):

        return self.name




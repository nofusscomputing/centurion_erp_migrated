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
        blank=False,
        help_text = 'Id of this item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this item',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    slug = AutoSlugField()

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class SoftwareCategory(SoftwareCommonFields, SaveHistory):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Software Category'

        verbose_name_plural = 'Software Categories'


    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
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
        "name",
        "organization",
        "created",
        "modified",
    ]


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
        blank= True,
        default = None,
        help_text = 'Who publishes this software',
        null = True,
        on_delete=models.SET_DEFAULT,
        verbose_name = 'Publisher',
    )

    category = models.ForeignKey(
        SoftwareCategory,
        blank= True,
        default = None,
        help_text = 'Category of this Softwarae',
        null = True,
        on_delete=models.SET_DEFAULT,
        verbose_name = 'Category'

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
                    "field": "version",
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


    table_fields: list = [
        "name",
        "publisher",
        "category",
        "organization",
        "created",
        "modified",
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

        ordering = [
            'name'
        ]

        verbose_name = 'Software Version'

        verbose_name_plural = 'Software Versions'


    software = models.ForeignKey(
        Software,
        blank = False,
        help_text = 'Software this version applies',
        null = False,
        on_delete=models.CASCADE,
        verbose_name = 'Software',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of for the software version',
        max_length = 50,
        unique = False,
        verbose_name = 'Name'
    )

    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified',
    ]


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.software


    def __str__(self):

        return self.name




from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from rest_framework.reverse import reverse

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory
from core.models.manufacturer import Manufacturer
from core.signal.ticket_linked_item_delete import TicketLinkedItem, deleted_model

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
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
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
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
                }
            ]
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


    def get_url( self, request = None ) -> str:

        if request:

            return reverse("v2:_api_v2_software-detail", request=request, kwargs={'pk': self.id})

        return reverse("v2:_api_v2_software-detail", kwargs={'pk': self.id})


    def __str__(self):

        return self.name



@receiver(post_delete, sender=Software, dispatch_uid='software_delete_signal')
def signal_deleted_model(sender, instance, using, **kwargs):

    deleted_model.send(sender='software_deleted', item_id=instance.id, item_type = TicketLinkedItem.Modules.SOFTWARE)



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

    # model does not have it's own page
    # as it's a secondary model. 
    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'software',
                        'name',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                        'is_virtual',
                        'is_global',
                    ]
                },
            ]
        },
        {
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
                }
            ]
        },
        {
            "name": "Tickets",
            "slug": "tickets",
            "sections": [
                # {
                #     "layout": "table",
                #     "field": "tickets",
                # }
            ],
        },

    ]

    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified',
    ]


    def get_url_kwargs(self) -> dict:

        return {
            'software_id': self.software.id,
            'pk': self.id
        }


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.software


    def __str__(self):

        return self.name




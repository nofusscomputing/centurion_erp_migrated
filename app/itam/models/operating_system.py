from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from rest_framework.reverse import reverse

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory
from core.models.manufacturer import Manufacturer
from core.signal.ticket_linked_item_delete import TicketLinkedItem, deleted_model



class OperatingSystemCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'ID of this item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class OperatingSystemFieldsName(OperatingSystemCommonFields):

    class Meta:
        abstract = True

    name = models.CharField(
        blank = False,
        help_text = 'Name of this item',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    slug = AutoSlugField()



class OperatingSystem(OperatingSystemFieldsName, SaveHistory):


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Operating System'

        verbose_name_plural = 'Operating Systems'


    publisher = models.ForeignKey(
        Manufacturer,
        blank = True,
        default = None,
        help_text = 'Who publishes this Operating System',
        null = True,
        on_delete = models.SET_DEFAULT,
        verbose_name = 'Publisher'
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
        #             "field": "licence",
        #         }
        #     ]
        # },
        {
            "name": "Installations",
            "slug": "installs",
            "sections": [
                {
                    "layout": "table",
                    "field": "installations",
                }
            ]
        },
        {
            "name": "Tickets",
            "slug": "ticket",
            "sections": [
                {
                    "layout": "table",
                    "field": "tickets",
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
        'publisher',
        'organization',
        'created',
        'modified'
    ]


    def get_url( self, request = None ) -> str:

        if request:

            return reverse("v2:_api_v2_operating_system-detail", request=request, kwargs={'pk': self.id})

        return reverse("v2:_api_v2_operating_system-detail", kwargs={'pk': self.id})


    def __str__(self):

        return self.name



@receiver(post_delete, sender=OperatingSystem, dispatch_uid='operating_system_delete_signal')
def signal_deleted_model(sender, instance, using, **kwargs):

    deleted_model.send(sender='operating_system_deleted', item_id=instance.id, item_type = TicketLinkedItem.Modules.OPERATING_SYSTEM)



class OperatingSystemVersion(OperatingSystemCommonFields, SaveHistory):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Operating System Version'

        verbose_name_plural = 'Operating System Versions'


    operating_system = models.ForeignKey(
        OperatingSystem,
        help_text = 'Operating system this version applies to',
        on_delete = models.CASCADE,
        verbose_name = 'Operating System'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Major version number for the Operating System',
        max_length = 50,
        unique = False,
        verbose_name = 'Major Version',
    )

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'operating_system',
                        'name',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                        'is_global',
                    ]
                },
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
        'installations',
        'created',
        'modified',
    ]


    def get_url_kwargs(self) -> dict:

        return {
            'operating_system_id': self.operating_system.id,
            'pk': self.id
        }


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.operating_system


    def __str__(self):

        return self.operating_system.name + ' ' + self.name


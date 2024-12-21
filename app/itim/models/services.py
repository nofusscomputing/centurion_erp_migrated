import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.forms import ValidationError

from rest_framework.reverse import reverse

from access.fields import *
from access.models import Team, TenancyObject

from core.signal.ticket_linked_item_delete import TicketLinkedItem, deleted_model

from itam.models.device import Device

from itim.models.clusters import Cluster



class Port(TenancyObject):


    class Meta:

        ordering = [
            'number',
            'protocol',
        ]

        verbose_name = "Port"

        verbose_name_plural = "Ports"


    class Protocol(models.TextChoices):
        TCP = 'TCP', 'TCP'
        UDP = 'UDP', 'UDP'

    def validation_port_number(number: int):

        if number < 1 or number > 65535:

            raise ValidationError('A Valid port number is between 1-65535')


    id = models.AutoField(
        blank=False,
        help_text = 'ID of this port',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    number = models.IntegerField(
        blank = False,
        help_text = 'The port number',
        unique = False,
        validators = [ validation_port_number ],
        verbose_name = 'Port Number',
    )

    description = models.CharField(
        blank = True,
        default = None,
        help_text = 'Short description of port',
        max_length = 80,
        null = True,
        verbose_name = 'Description',
    )

    protocol = models.CharField(
        blank = False,
        choices=Protocol.choices,
        help_text = 'Layer 4 Network Protocol',
        max_length = 3,
        verbose_name = 'Protocol',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'display_name',
                        'description',
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
            ]
        },
        {
            "name": "Services",
            "slug": "services",
            "sections": [
                {
                    "layout": "table",
                    "field": "services",
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
        },
    ]


    table_fields: list = [
        'display_name',
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return str(self.protocol) + '/' + str(self.number)



class Service(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Service"

        verbose_name_plural = "Services"

    def validate_config_key_variable(value):

        if not value:

            raise ValidationError('You must enter a config key.')

        valid_chars = search=re.compile(r'[^a-z_]').search

        if bool(valid_chars(value)):

            raise ValidationError('config key must only contain [a-z_].')


    id = models.AutoField(
        blank=False,
        help_text = 'Id for this Service',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    is_template = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this service to be used as a template',
        verbose_name = 'Template',
    )

    template = models.ForeignKey(
        'self',
        blank = True,
        default = None,
        help_text = 'Template this service uses',
        null = True,
        on_delete = models.CASCADE,
        verbose_name = 'Template Name',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Service',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    device = models.ForeignKey(
        Device,
        blank = True,
        default = None,
        help_text = 'Device the service is assigned to',
        null = True,
        on_delete = models.CASCADE,
        verbose_name = 'Device',
    )

    cluster = models.ForeignKey(
        'Cluster',
        blank = True,
        default = None,
        help_text = 'Cluster the service is assigned to',
        null = True,
        on_delete = models.CASCADE,
        unique = False,
        verbose_name = 'Cluster',
    )

    config = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Cluster Configuration',
        null = True,
        verbose_name = 'Configuration',
    )

    config_key_variable = models.CharField(
        blank = True,
        help_text = 'Key name to use when merging with cluster/device config.',
        max_length = 50,
        null = True,
        unique = False,
        validators = [ validate_config_key_variable ],
        verbose_name = 'Configuration Key',
    )

    port = models.ManyToManyField(
        Port,
        blank = True,
        help_text = 'Port the service is available on',
        verbose_name = 'Port',
    )

    dependent_service = models.ManyToManyField(
        'self',
        blank = True,
        default = None,
        help_text = 'Services that this service depends upon',
        related_name = 'dependentservice',
        symmetrical = False,
        verbose_name = 'Dependent Services',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


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
                        'config_key_variable',
                        'template',
                        'is_template',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
                {
                    "name": "cluster / Device",
                    "layout": "double",
                    "left": [
                        'cluster',
                    ],
                    "right": [
                        'device',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'config',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'dependent_service'
                    ]
                },
                {
                    "layout": "single",
                    "name": "Ports",
                    "fields": [
                        'port'
                    ],
                }
            ]
        },
        {
            "name": "Rendered Config",
            "slug": "config_management",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        "rendered_config",
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
        'deployed_to'
        'organization',
        'created',
        'modified'
    ]


    def get_url( self, request = None ) -> str:

        if request:

            return reverse("v2:_api_v2_service-detail", request=request, kwargs={'pk': self.id})

        return reverse("v2:_api_v2_service-detail", kwargs={'pk': self.id})


    @property
    def config_variables(self):

        config: dict = {}


        if self.template:

            if self.template.config:

                config.update(self.template.config)


        if self.config:

            config.update(self.config)

        return config



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.config_key_variable:

            self.config_key_variable = self.config_key_variable.lower()

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    def __str__(self):

        return self.name



@receiver(post_delete, sender=Service, dispatch_uid='service_delete_signal')
def signal_deleted_model(sender, instance, using, **kwargs):

    deleted_model.send(sender='service_deleted', item_id=instance.id, item_type = TicketLinkedItem.Modules.SERVICE)

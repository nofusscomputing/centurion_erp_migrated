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



class ClusterType(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Cluster Type"

        verbose_name_plural = "Cluster Types"


    id = models.AutoField(
        blank=False,
        help_text = 'ID for this cluster type',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Cluster Type',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    slug = AutoSlugField()


    config = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Cluster Type Configuration that is applied to all clusters of this type',
        null = True,
        verbose_name = 'Configuration',
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
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'config',
                    ]
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
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return self.name



class Cluster(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Cluster"

        verbose_name_plural = "Clusters"


    id = models.AutoField(
        blank=False,
        help_text = 'ID for this cluster',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    parent_cluster = models.ForeignKey(
        'self',
        blank = True,
        default = None,
        help_text = 'Parent Cluster for this cluster',
        null = True,
        on_delete = models.SET_DEFAULT,
        verbose_name = 'Parent Cluster',
    )

    cluster_type = models.ForeignKey(
        ClusterType,
        blank = True,
        default = None,
        help_text = 'Type of Cluster',
        null = True,
        on_delete = models.SET_DEFAULT,
        verbose_name = 'Cluster Type',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Cluster',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    slug = AutoSlugField()

    config = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Cluster Configuration',
        null = True,
        verbose_name = 'Configuration',
    )

    nodes = models.ManyToManyField(
        Device,
        blank = True,
        default = None,
        help_text = 'Hosts for resource consumption that the cluster is deployed upon',
        related_name = 'cluster_node',
        verbose_name = 'Nodes',
    )

    devices = models.ManyToManyField(
        Device,
        blank = True,
        default = None,
        help_text = 'Devices that are deployed upon the cluster.',
        related_name = 'cluster_device',
        verbose_name = 'Devices',
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
                        'parent_cluster',
                        'cluster_type',
                        'name',
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'resources',
                        'created',
                        'modified',
                    ]
                },
                {
                    "layout": "double",
                    "name": "Nodes / Devices",
                    "left": [
                        'nodes',
                    ],
                    "right": [
                        'devices',
                    ]
                },
                {
                    "layout": "table",
                    "name": "Services",
                    "field": "service",
                },
                {
                    "layout": "single",
                    "fields": [
                        'config',
                    ]
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
        'parent_cluster',
        'cluster_type',
        'organization',
        'created',
        'modified'
    ]


    def get_url( self, request = None ) -> str:

        if request:

            return reverse("v2:_api_v2_cluster-detail", request=request, kwargs={'pk': self.id})

        return reverse("v2:_api_v2_cluster-detail", kwargs={'pk': self.id})


    @property
    def rendered_config(self):

        from itim.models.services import Service

        rendered_config: dict = {}

        if self.cluster_type:

            if self.cluster_type.config:

                rendered_config.update(
                    self.cluster_type.config
                )


        for service in Service.objects.filter(cluster = self.pk):

            if service.config_variables:

                rendered_config.update( service.config_variables )


        if self.config:

            rendered_config.update(
                self.config
            )



        return rendered_config


    def __str__(self):

        return self.name



@receiver(post_delete, sender=Cluster, dispatch_uid='cluster_delete_signal')
def signal_deleted_model(sender, instance, using, **kwargs):

    deleted_model.send(sender='cluster_deleted', item_id=instance.id, item_type = TicketLinkedItem.Modules.CLUSTER)

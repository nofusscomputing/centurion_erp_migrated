from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from access.fields import *
from access.models import Team, TenancyObject

from itam.models.device import Device



class ClusterType(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "ClusterType"

        verbose_name_plural = "ClusterTypes"


    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Cluster Type',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    slug = AutoSlugField()



class Cluster(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Cluster"

        verbose_name_plural = "Clusters"


    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    parent_cluster = models.ForeignKey(
        'self',
        blank = True,
        default = None,
        help_text = 'Parent Cluster for this cluster',
        null = True,
        on_delete = models.CASCADE,
        verbose_name = 'Parent Cluster',
    )

    cluster_type = models.ForeignKey(
        ClusterType,
        blank = True,
        default = None,
        help_text = 'Parent Cluster for this cluster',
        null = True,
        on_delete = models.CASCADE,
        verbose_name = 'Parent Cluster',
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

    node = models.ManyToManyField(
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


    def __str__(self):

        return self.name

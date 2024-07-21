import re

from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from access.fields import *
from access.models import Team, TenancyObject

from itam.models.device import Device

from itim.models.clusters import Cluster



class Port(TenancyObject):


    class Meta:

        ordering = [
            'number',
            'protocol',
        ]

        verbose_name = "Protocol"

        verbose_name_plural = "Protocols"


    class Protocol(models.TextChoices):
        TCP = 'TCP', 'TCP'
        UDP = 'UDP', 'UDP'

    def validation_port_number(number: int):

        if number < 1 or number > 65535:

            raise ValidationError('A Valid port number is between 1-65535')


    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
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
        default = Protocol.TCP,
        help_text = 'Layer 4 Network Protocol',
        max_length = 3,
        verbose_name = 'Protocol',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


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
        primary_key=True,
        unique=True,
        blank=False
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
        blank = False,
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

    @property
    def config_variables(self):

        if self.is_template:

            return self.config

        if self.template:

            template_config: dict = Service.objects.get(id=self.template.id).config

            template_config.update(self.config)

            return template_config

        else:

            return self.config

        return None


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.config_key_variable:

            self.config_key_variable = self.config_key_variable.lower()

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    def __str__(self):

        return self.name

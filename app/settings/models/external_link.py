from django.template import Template

from access.fields import *
from access.models import TenancyObject



class ExternalLink(TenancyObject):

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    name = models.CharField(
        blank = False,
        max_length = 30,
        unique = True,
        help_text = 'Name to display on link button',
        verbose_name = 'Button Name',
    )

    slug = None

    template = models.CharField(
        blank = False,
        max_length = 180,
        unique = False,
        help_text = 'External Link template',
        verbose_name = 'Link Template',
    )

    colour = models.CharField(
        blank = True,
        null = True,
        default = None,
        max_length = 80,
        unique = False,
        help_text = 'Colour to render the link button. Use HTML colour code',
        verbose_name = 'Button Colour',
    )

    devices = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Render link for devices',
        verbose_name = 'Devices',
    )

    software = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Render link for software',
        verbose_name = 'Software',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def __str__(self):
        """ Return the Template to render """

        return str(self.template)

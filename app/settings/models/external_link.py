from django.template import Template

from access.fields import *
from access.models import TenancyObject



class ExternalLink(TenancyObject):


    class Meta:

        ordering = [
            'name',
            'organization',
        ]

        verbose_name = 'External Link'

        verbose_name_plural = 'External Links'


    id = models.AutoField(
        blank=False,
        help_text = 'ID for this external link',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name to display on link button',
        max_length = 30,
        unique = True,
        verbose_name = 'Button Name',
    )

    slug = None

    template = models.CharField(
        blank = False,
        help_text = 'External Link template',
        max_length = 180,
        unique = False,
        verbose_name = 'Link Template',
    )

    colour = models.CharField(
        blank = True,
        default = None,
        help_text = 'Colour to render the link button. Use HTML colour code',
        max_length = 80,
        null = True,
        unique = False,
        verbose_name = 'Button Colour',
    )

    cluster = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Render link for clusters',
        verbose_name = 'Clusters',
    )

    devices = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Render link for devices',
        verbose_name = 'Devices',
    )

    service = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Render link for service',
        verbose_name = 'Service',
    )

    software = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Render link for software',
        verbose_name = 'Software',
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
                        'template',
                        'colour',
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
                {
                    "name": "Assignable to",
                    "layout": "double",
                    "left": [
                        'cluster',
                        'service',
                    ],
                    "right": [
                        'devices',
                        'software',
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
        },
    ]


    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):
        """ Return the Template to render """

        return str(self.template)

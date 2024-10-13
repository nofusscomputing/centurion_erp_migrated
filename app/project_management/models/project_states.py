from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models import TenancyObject, Team

from assistance.models.knowledge_base import KnowledgeBase



class ProjectStateCommonFields(TenancyObject):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'State ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class ProjectState(ProjectStateCommonFields):


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = "Project State"

        verbose_name_plural = "Project States"


    name = models.CharField(
        blank = False,
        help_text = "Name of thee project state.",
        max_length = 50,
        unique = True,
        verbose_name = 'Name',
    )

    runbook = models.ForeignKey(
        KnowledgeBase,
        blank= True,
        help_text = 'The runbook for this project state',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Runbook',
    )


    is_completed = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this state considered complete',
        null = False,
        verbose_name = 'State Completed',
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
                        'name'
                        'runbook',
                        'is_global',
                        'is_completed',
                    ],
                    "right": [
                        'model_notes'
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
        },
    ]

    def __str__(self):

        return self.name

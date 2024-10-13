from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models import TenancyObject, Team

from assistance.models.knowledge_base import KnowledgeBase



class TicketCommentCategoryCommonFields(TenancyObject):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'Category ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class TicketCommentCategory(TicketCommentCategoryCommonFields):


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = "Ticket Comment Category"

        verbose_name_plural = "Ticket Comment Categories"


    parent = models.ForeignKey(
        'self',
        blank= True,
        help_text = 'The Parent Category',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Parent Category',
    )

    name = models.CharField(
        blank = False,
        help_text = "Category Name",
        max_length = 50,
        verbose_name = 'Name',
    )

    runbook = models.ForeignKey(
        KnowledgeBase,
        blank= True,
        help_text = 'The runbook for this category',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Runbook',
    )

    comment = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for standard comment',
        null = False,
        verbose_name = 'Comment',
    )

    notification = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for notification comment',
        null = False,
        verbose_name = 'Notification Comment',
    )

    solution = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for solution comment',
        null = False,
        verbose_name = 'Solution Comment',
    )

    task = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for task comment',
        null = False,
        verbose_name = 'Task Comment',
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
                        'parent'
                        'name'
                        'runbook',
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
                {
                    "layout": "double",
                    "left": [
                        'comment',
                        'solution'
                    ],
                    "right": [
                        'notification',
                        'task',
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

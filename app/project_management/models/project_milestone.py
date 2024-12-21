from django.contrib.auth.models import User
from django.db import models

from access.fields import AutoCreatedField

from .projects import Project, ProjectCommonFieldsName, SaveHistory



class ProjectMilestone(ProjectCommonFieldsName):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Project Milestone'

        verbose_name_plural = 'Project Milestones'


    description = models.TextField(
        blank = True,
        default = None,
        help_text = 'Description of milestone. Markdown supported',
        null= True,
        verbose_name = 'Description',
    )

    start_date = models.DateTimeField(
        blank = True,
        help_text = 'When work commenced on the project.',
        null = True,
        verbose_name = 'Real Start Date',
    )

    finish_date = models.DateTimeField(
        blank = True,
        help_text = 'When work was completed for the project',
        null = True,
        verbose_name = 'Real Finish Date',
    )

    project = models.ForeignKey(
        Project,
        blank= False,
        help_text = 'Project this milestone belongs.',
        on_delete=models.CASCADE,
        null = False,
    )

    model_notes = None


    created = AutoCreatedField(
        editable = False,
    )


    # model not intended to be vieable on its own page
    # as this model is a sub-model.
    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'project',
                        'name',
                        'start_date',
                        'finish_date',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'description',
                        'is_global',
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
        'percent_completed'
        'start_date',
        'finish_date',
    ]


    def __str__(self):

        return self.name


    def get_url_kwargs(self) -> dict:

        return {
            'project_id': self.project.id,
            'pk': self.id
        }


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.project


    @property
    def percent_completed(self) -> str: # Auto-Calculate
        """ How much of the milestone is completed.

        Returns:
            str: Calculated percentage of project completion.
        """

        return 'xx %'

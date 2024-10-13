from django.contrib.auth.models import User
from django.db import models

from access.models import Team

from core.mixin.history_save import SaveHistory
from core.models.ticket.ticket_enum_values import TicketValues

from .project_common import ProjectCommonFieldsName
from .project_states import ProjectState
from .project_types import ProjectType


class Project(ProjectCommonFieldsName):


    class Meta:

        ordering = [
            'code',
            'name',
        ]

        permissions = [
            ('import_project', 'Can import a project'),
        ]

        verbose_name = 'Project'

        verbose_name_plural = 'Projects'


    class Ticket_ExternalSystem(models.IntegerChoices): # <null|github|gitlab>
        GITHUB   = TicketValues.ExternalSystem._GITHUB_INT, TicketValues.ExternalSystem._GITHUB_VALUE
        GITLAB   = TicketValues.ExternalSystem._GITLAB_INT, TicketValues.ExternalSystem._GITLAB_VALUE

        CUSTOM_1 = TicketValues.ExternalSystem._CUSTOM_1_INT, TicketValues.ExternalSystem._CUSTOM_1_VALUE
        CUSTOM_2 = TicketValues.ExternalSystem._CUSTOM_2_INT, TicketValues.ExternalSystem._CUSTOM_2_VALUE
        CUSTOM_3 = TicketValues.ExternalSystem._CUSTOM_3_INT, TicketValues.ExternalSystem._CUSTOM_3_VALUE
        CUSTOM_4 = TicketValues.ExternalSystem._CUSTOM_4_INT, TicketValues.ExternalSystem._CUSTOM_4_VALUE
        CUSTOM_5 = TicketValues.ExternalSystem._CUSTOM_5_INT, TicketValues.ExternalSystem._CUSTOM_5_VALUE
        CUSTOM_6 = TicketValues.ExternalSystem._CUSTOM_6_INT, TicketValues.ExternalSystem._CUSTOM_6_VALUE
        CUSTOM_7 = TicketValues.ExternalSystem._CUSTOM_7_INT, TicketValues.ExternalSystem._CUSTOM_7_VALUE
        CUSTOM_8 = TicketValues.ExternalSystem._CUSTOM_8_INT, TicketValues.ExternalSystem._CUSTOM_8_VALUE
        CUSTOM_9 = TicketValues.ExternalSystem._CUSTOM_9_INT, TicketValues.ExternalSystem._CUSTOM_9_VALUE



    class Priority(models.IntegerChoices):
        VERY_LOW  = TicketValues.Priority._VERY_LOW_INT, TicketValues.Priority._VERY_LOW_VALUE
        LOW       = TicketValues.Priority._LOW_INT, TicketValues.Priority._LOW_VALUE
        MEDIUM    = TicketValues.Priority._MEDIUM_INT, TicketValues.Priority._MEDIUM_VALUE
        HIGH      = TicketValues.Priority._HIGH_INT, TicketValues.Priority._HIGH_VALUE
        VERY_HIGH = TicketValues.Priority._VERY_HIGH_INT, TicketValues.Priority._VERY_HIGH_VALUE
        MAJOR     = TicketValues.Priority._MAJOR_INT, TicketValues.Priority._MAJOR_VALUE


    # class ProjectStates(enum):
    #     OPEN = 1
    #     CLOSED = 1

    external_ref = models.IntegerField(
        blank = True,
        default=None,
        help_text = 'External System reference',
        null=True,
        verbose_name = 'Reference Number',
    ) # external reference or null. i.e. github issue number


    external_system = models.IntegerField(
        blank = True,
        choices=Ticket_ExternalSystem,
        default=None,
        help_text = 'External system this item derives',
        null=True,
        verbose_name = 'External System',
    ) 


    description = models.TextField(
        blank = True,
        default = None,
        null= True,
    )

    priority = models.IntegerField(
        blank = False,
        choices =Priority,
        default = Priority.LOW,
        help_text = 'Priority of the project',
        null = True,
        verbose_name ='Priority'
    )

    state = models.ForeignKey(
        ProjectState,
        blank= True,
        help_text = 'State of the project',
        on_delete=models.SET_NULL,
        null = True,
        verbose_name ='Project State'
    )


    project_type = models.ForeignKey(
        ProjectType,
        blank= True,
        help_text = 'Type of project',
        on_delete=models.SET_NULL,
        null = True,
        verbose_name ='Project Type'
    )

    code = models.CharField(
        blank = True,
        help_text = 'Project Code',
        max_length = 25,
        null = True,
        unique = True,
        verbose_name = 'Project Code',
    )

    planned_start_date = models.DateTimeField(
        blank = True,
        help_text = 'When the project is planned to have been started by.',
        null = True,
        verbose_name = 'Planned Start Date',
    )

    planned_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'When the project is planned to be finished by.',
        null = True,
        verbose_name = 'Planned Finish Date',
    )

    real_start_date = models.DateTimeField(
        blank = True,
        help_text = 'When work commenced on the project.',
        null = True,
        verbose_name = 'Real Start Date',
    )

    real_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'When work was completed for the project',
        null = True,
        verbose_name = 'Real Finish Date',
    )

    manager_user = models.ForeignKey(
        User,
        blank= True,
        help_text = '',
        on_delete=models.SET_NULL,
        null = True,
        related_name = 'manager_user'
    )

    manager_team =  models.ForeignKey(
        Team,
        blank= True,
        help_text = '',
        on_delete=models.SET_NULL,
        null = True,
    )

    model_notes = None

    team_members = models.ManyToManyField(
        to = User,
        blank = True,
    )

    is_deleted = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this project considered deleted',
        null = False,
        verbose_name = 'Deleted',
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
                        'code',
                        'name'
                        'priority',
                        'project_type',
                        'state',
                        'percent_completed',
                    ],
                    "right": [
                        'planned_start_date',
                        'planned_finish_date',
                        'real_start_date',
                        'real_finish_date',
                        'duration_project'
                        'created',
                        'modified',
                    ]
                },
                {
                    "layout": "double",
                    "left": [
                        'manager_user',
                    ],
                    "right": [
                        'manager_team',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'description'
                    ]
                }
            ]
        },
        {
            "name": "Tasks",
            "slug": "ticket",
            "sections": [
                {
                    "layout": "table",
                    "field": "tickets",
                }
            ]
        },
        {
            "name": "Milestones",
            "slug": "milestones",
            "sections": [
                {
                    "layout": "table",
                    "field": "milestones",
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]


    fields_all: list = []

    fields_import: list = []



    def __str__(self):

        return self.name


    @property
    def duration_project(self) -> int:

        duration_project: int = 0

        from core.models.ticket.ticket import Ticket

        tickets = Ticket.objects.filter(
            project = self.id
        )

        for ticket in tickets:

            duration_project = duration_project + int(ticket.duration_ticket)


        return int(duration_project)


    @property
    def percent_completed(self) -> str: # Auto-Calculate
        """ How much of the project is completed.

        Returns:
            str: Calculated percentage of project completion.
        """

        from core.models.ticket.ticket import Ticket

        ticket_status_closed = [
            TicketValues._CANCELLED_INT,
            TicketValues._CLOSED_INT,
            TicketValues._SOLVED_INT,
        ]

        all_tickets = Ticket.objects.filter(
            project = self.id,
        ).exclude(
            status__in = ticket_status_closed
        )

        closed_tickets = Ticket.objects.filter(
            project = self.id,
            status__in = ticket_status_closed
        )

        calculation: int = 0

        if len(all_tickets) > 0:

            if len(closed_tickets) > 0:

                calculation: int = int(
                    (
                        len(closed_tickets) / len(all_tickets)
                    ) * 100
                )

        return str(calculation) + '%'


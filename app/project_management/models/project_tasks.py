from django.contrib.auth.models import User
from django.db import models

from .projects import Project
from .project_common import ProjectCommonFieldsName

from access.models import Team

from core.mixin.history_save import SaveHistory



class ProjectTask(ProjectCommonFieldsName):


    class Meta:

        ordering = [
            'code',
            'name',
        ]

        verbose_name = 'Project Task'

        verbose_name_plural = 'Project Tasks'



    # class ProjectTaskStates(enum):
    #     OPEN = 1
    #     CLOSED = 1


    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null = False,
        blank= False
    )
    
    parent_task = models.ForeignKey(
        'self',
        blank= True,
        default = None,
        on_delete=models.CASCADE,
        null = True,
    )

    description = models.TextField(
        blank = True,
        default = None,
        null= True,
    )

    # priority

    # state

    # percent_done

    # task_type

    code = models.CharField(
        blank = False,
        help_text = 'Project Code',
        max_length = 25,
        unique = True,
    )

    planned_start_date = models.DateTimeField(
        blank = True,
        help_text = 'When the task is planned to have been started by.',
        null = True,
        verbose_name = 'Planned Start Date',
    )

    planned_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'When the task is planned to be finished by.',
        null = True,
        verbose_name = 'Planned Finish Date',
    )

    real_start_date = models.DateTimeField(
        blank = True,
        help_text = 'When work commenced on the task.',
        null = True,
        verbose_name = 'Real Start Date',
    )

    real_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'When work was completed for the task',
        null = True,
        verbose_name = 'Real Finish Date',
    )

    milestone = models.BooleanField(
        blank = False,
        help_text = 'Is this task a milestone?',
        default = False,
    )

    model_notes = None

    task_owner = models.ForeignKey(
        User,
        blank= True,
        help_text = 'User whom is considered the task owner.',
        on_delete=models.SET_NULL,
        null = True,
        verbose_name = 'Task Owner',
    )

    task_members = models.ManyToManyField(
        to = User,
        blank = False,
        help_text = 'User whom is responsible for completing the task.',
        related_name = 'task_members',
        verbose_name = 'Team Members',
    )
from django.db import models

from .projects import ProjectModel

from access.models import TenancyObject



class ProjectTaskModel(model.Model, TenancyObject):


    class Meta:

        ordering = [
            'code',
            'name',
        ]

        verbose_name = 'Project Task'

        verbose_name_plural = 'Project Tasks'



    class ProjectTaskStates(enum):
        OPEN = 1
        CLOSED = 1


    project
    
    parent_task

    name

    description

    priority

    state

    percent_done

    task_type

    code

    planned_start_date

    planned_finish_date

    real_start_date

    milestone = models.BooleanField(
        blank = False,
        default = False,
    )



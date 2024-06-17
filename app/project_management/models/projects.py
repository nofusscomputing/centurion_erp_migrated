from django.db import models

from access.models import TenancyObject


class ProjectModel(TenancyObject):


    class Meta:

        ordering = [
            'code',
            'name',
        ]

        verbose_name = 'Project'

        verbose_name_plural = 'Projects'



    class ProjectStates(enum):
        OPEN = 1
        CLOSED = 1


    name

    description

    priority

    state

    percent_done # Auto-Calculate

    project_type

    code

    planned_start_date

    planned_finish_date

    real_start_date



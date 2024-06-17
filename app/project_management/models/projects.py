from django.db import models

from core.mixin.history_save import SaveHistory

from .project_common import ProjectCommonFieldsName


class Project(ProjectCommonFieldsName, SaveHistory):


    class Meta:

        ordering = [
            'code',
            'name',
        ]

        verbose_name = 'Project'

        verbose_name_plural = 'Projects'


    # class ProjectStates(enum):
    #     OPEN = 1
    #     CLOSED = 1


    description = models.TextField(
        blank = True,
        default = None,
        null= True,
    )

    # priority

    # state


    # project_type

    code = models.CharField(
        blank = False,
        help_text = 'Project Code',
        max_length = 25,
        unique = True,
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

    model_notes = None


    @property
    def percent_completed(self) -> str: # Auto-Calculate
        """ How much of the project is completed.

        Returns:
            str: Calculated percentage of project completion.
        """

        return 'xx %'


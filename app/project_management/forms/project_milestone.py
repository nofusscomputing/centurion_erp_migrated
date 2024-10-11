from django import forms
from django.urls import reverse
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm
from core.templatetags.markdown import to_duration

from project_management.models.project_milestone import ProjectMilestone



class ProjectMilestoneForm(CommonModelForm):

    prefix = 'project'

    class Meta:
        fields = [
            'id',
            'organization',
            'name',
            'description',
            'project',
            'start_date',
            'finish_date',
        ]


        model = ProjectMilestone


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'format': "%Y-%m-%dT%H:%M"})
        self.fields['start_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['start_date'].format="%Y-%m-%dT%H:%M"

        self.fields['finish_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['finish_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['finish_date'].format="%Y-%m-%dT%H:%M"

        self.fields['description'].widget.attrs = {'style': "height: 800px; width: 1000px"}

        self.fields['project'].widget = self.fields['project'].hidden_widget()


class DetailForm(ProjectMilestoneForm):


    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'percent_completed',
                        'organization'
                        'c_created',
                        'c_modified',
                    ],
                    "right": [
                        'start_date',
                        'finish_date',
                    ]
                },
                {
                    "layout": "single",
                    "name": "Description",
                    "fields": [
                        'description',
                    ],
                    "markdown": [
                        'description',
                    ],
                },
            ]
        },
        "tasks": {
            "name": "Tasks",
            "slug": "tasks",
            "sections": []
        },
    }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['c_created'] = forms.DateTimeField(
            label = 'Created',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.created,
        )

        self.fields['c_modified'] = forms.DateTimeField(
            label = 'Modified',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.modified,
        )

        self.url_index_view = reverse('Project Management:_project_view', kwargs={'pk': self.instance.project.id}) + '?tab=milestones'

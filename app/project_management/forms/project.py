from django import forms
from django.urls import reverse
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm
from core.templatetags.markdown import to_duration

from project_management.models.projects import Project



class ProjectForm(CommonModelForm):

    prefix = 'project'

    class Meta:
        fields = '__all__'


        model = Project


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['planned_start_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'format': "%Y-%m-%dT%H:%M"})
        self.fields['planned_start_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['planned_start_date'].format="%Y-%m-%dT%H:%M"

        self.fields['planned_finish_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['planned_finish_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['planned_finish_date'].format="%Y-%m-%dT%H:%M"

        self.fields['real_start_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['real_start_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['real_start_date'].format="%Y-%m-%dT%H:%M"

        self.fields['real_finish_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['real_finish_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['real_finish_date'].format="%Y-%m-%dT%H:%M"

        self.fields['description'].widget.attrs = {'style': "height: 800px; width: 1000px"}


class DetailForm(ProjectForm):


    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'code',
                        'name',
                        'priority',
                        'project_type',
                        'state',
                        'completed',
                        'organization'
                    ],
                    "right": [
                        'planned_start_date',
                        'planned_finish_date',
                        'real_start_date',
                        'real_finish_date',
                        'duration'
                    ]
                },
                {
                    "layout": "double",
                    "name": "Manager",
                    "left": [
                        'manager_user',
                    ],
                    "right": [
                        'manager_team',
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
        "milestones": {
            "name": "Milestones",
            "slug": "milestones",
            "sections": []
        },
        "notes": {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
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

        self.fields['duration'] = forms.IntegerField(
            label = 'Duration',
            disabled = True,
            initial = to_duration(self.instance.duration_project),
        )

        self.fields['completed'] = forms.CharField(
            disabled = True,
            help_text = 'Project completion percentage.',
            initial = self.instance.percent_completed,
            label = 'Completed',
        )

        self.tabs['details'].update({
            "edit_url": reverse('Project Management:_project_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('Project Management:Projects')

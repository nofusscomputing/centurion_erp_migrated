from django import forms
from django.urls import reverse
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm
from core.templatetags.markdown import to_duration

from project_management.models.project_states import ProjectState



class ProjectStateForm(CommonModelForm):

    class Meta:

        fields = [
            'id',
            'organization',
            'name',
            'model_notes',
            'runbook'
        ]

        model = ProjectState


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # self.fields['description'].widget.attrs = {'style': "height: 800px; width: 1000px"}


class DetailForm(ProjectStateForm):


    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'runbook',
                        'organization',
                        'c_created',
                        'c_modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
            ]
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

        self.tabs['details'].update({
            "edit_url": reverse('Settings:_project_state_change', args=(self.instance.pk,))
        })
        self.url_index_view = reverse('Settings:_project_states')

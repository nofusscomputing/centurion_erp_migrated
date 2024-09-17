
from django import forms
from django.urls import reverse

from app import settings

from core.forms.common import CommonModelForm

from project_management.models.project_types import ProjectType



class ProjectTypeForm(CommonModelForm):


    class Meta:

        fields = '__all__'

        model = ProjectType

    prefix = 'project_type'


    def clean(self):
        
        cleaned_data = super().clean()

        return cleaned_data



class DetailForm(ProjectTypeForm):

    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'name',
                        'runbook',
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
            "edit_url": reverse('Settings:_project_type_change', kwargs={'pk': self.instance.pk})
        })

        self.url_index_view = reverse('Settings:_project_types')

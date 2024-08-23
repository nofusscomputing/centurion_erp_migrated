from django import forms
from django.urls import reverse

from app import settings

from config_management.models.groups import ConfigGroups

from core.forms.common import CommonModelForm

from itam.models.software import Software, SoftwareVersion


class ConfigGroupForm(CommonModelForm):

    class Meta:
       model = ConfigGroups
       fields = [
        'name',
        'parent',
        'is_global',
        'organization',
        'model_notes',
        'config',
       ]


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        if hasattr(kwargs['instance'], 'id'):

            self.fields['parent'].queryset = self.fields['parent'].queryset.filter(
            ).exclude(
                id=int(kwargs['instance'].id)
            )



class DetailForm(ConfigGroupForm):

    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'parent',
                        'is_global',
                        'organization',
                        'c_created',
                        'c_modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'config',
                    ]
                }
            ]
        },
        "child_groups": {
            "name": "Child Groups",
            "slug": "child_groups",
            "sections": []
        },
        "hosts": {
            "name": "Hosts",
            "slug": "hosts",
            "sections": []
        },
        "software": {
            "name": "Software",
            "slug": "software",
            "sections": []
        },
        "configuration": {
            "name": "Configuration",
            "slug": "configuration",
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


        self.tabs['details'].update({
            "edit_url": reverse('Config Management:_group_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('Config Management:Groups')


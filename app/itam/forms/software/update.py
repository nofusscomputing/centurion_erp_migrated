from django import forms
from django.db.models import Q
from django.urls import reverse

from app import settings

from core.forms.common import CommonModelForm

from itam.models.software import Software



class SoftwareForm(CommonModelForm):

    class Meta:
        model = Software
        fields = [
            'name',
            'publisher',
            'slug',
            'category',
            'model_notes',
        ]


class SoftwareChange(SoftwareForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if not self.instance.is_global:


            self.fields['is_global'] = forms.BooleanField(
                label = 'Is Global',
                initial = self.instance.is_global
            )

            self.fields['organization'] = forms.CharField(
                label = 'Organization',
                initial = self.instance.organization
            )


class DetailForm(SoftwareForm):

    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'publisher',
                        'slug',
                        'organization',
                        'is_global',
                        'category',
                        'c_created',
                        'c_modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                }
            ]
        },
        "versions": {
            "name": "Versions",
            "slug": "versions",
            "sections": []
        },
        "licences": {
            "name": "Licences",
            "slug": "licences",
            "sections": []
        },
        "notes": {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
        "installations": {
            "name": "Installations",
            "slug": "installations",
            "sections": []
        }
    }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.fields[ 'organization' ] = forms.CharField(
            label = 'Organization',
            initial = self.instance.organization
        )


        if not self.instance.is_global:

            self.fields['is_global'].widget.attrs['disabled'] = True

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
            "edit_url": reverse('ITAM:_software_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('ITAM:Software')

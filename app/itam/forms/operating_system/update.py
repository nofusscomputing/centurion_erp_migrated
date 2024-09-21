from django import forms
from django.urls import reverse

from app import settings

from core.forms.common import CommonModelForm

from itam.models.operating_system import OperatingSystem



class OperatingSystemForm(CommonModelForm):

    class Meta:

        fields = [
            "name",
            'publisher',
            'slug',
            'id',
            'organization',
            'is_global',
            'model_notes',
        ]

        model = OperatingSystem



# class Update(OperatingSystemFormCommon):


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['_created'] = forms.DateTimeField(
#             label="Created",
#             input_formats=settings.DATETIME_FORMAT,
#             initial=kwargs['instance'].created,
#             disabled=True
#         )

#         self.fields['_modified'] = forms.DateTimeField(
#             label="Modified",
#             input_formats=settings.DATETIME_FORMAT,
#             initial=kwargs['instance'].modified,
#             disabled=True
#         )


#         if kwargs['instance'].is_global:

#             self.fields['is_global'].widget.attrs['disabled'] = True


class DetailForm(OperatingSystemForm):

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
                        'serial_number',
                        'organization',
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
        "installations": {
            "name": "Installations",
            "slug": "installations",
            "sections": []
        },
        "tickets": {
            "name": "Tickets",
            "slug": "tickets",
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
            "edit_url": reverse('ITAM:_operating_system_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('ITAM:Operating Systems')

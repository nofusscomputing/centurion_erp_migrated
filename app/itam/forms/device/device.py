from django import forms
from django.urls import reverse

from app import settings

from core.forms.common import CommonModelForm

from itam.models.device import Device


class DeviceForm(CommonModelForm):

    prefix = 'device'

    class Meta:
        model = Device
        fields = [
            'id',
            'name',
            'device_model',
            'serial_number',
            'uuid',
            'device_type',
            'organization',
            'is_virtual',
            'model_notes',
            'config',
        ]



class DetailForm(DeviceForm):

    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'device_model',
                        'serial_number',
                        'uuid',
                        'device_type',
                        'organization',
                        'c_created',
                        'c_modified',
                        'lastinventory',
                    ],
                    "right": [
                        'model_notes',
                        'is_virtual',
                    ]
                }
            ]
        },
        "software": {
            "name": "Software",
            "slug": "software",
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
        },
        "config_management": {
            "name": "Config Management",
            "slug": "config_management",
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

        self.fields['lastinventory'] = forms.DateTimeField(
                label="Last Inventory Date",
                input_formats=settings.DATETIME_FORMAT,
                initial=kwargs['instance'].inventorydate,
                disabled=True,
                required=False,
            )

        self.tabs['details'].update({
            "edit_url": reverse('ITAM:_device_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('ITAM:Devices')

from django import forms
from django.db.models import Q

from app import settings
from itam.models.device import Device


class DeviceForm(forms.ModelForm):

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
            'model_notes',
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['_lastinventory'] = forms.DateTimeField(
            label="Last Inventory Date",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].inventorydate,
            disabled=True,
            required=False,
        )

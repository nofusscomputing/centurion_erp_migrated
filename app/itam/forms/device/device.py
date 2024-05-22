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
            'serial_number',
            'uuid',
            'device_type',
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

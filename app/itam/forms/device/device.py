from django import forms
from django.db.models import Q

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

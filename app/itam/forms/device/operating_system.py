from django import forms
from django.db.models import Q

from itam.models.device import DeviceOperatingSystem


class Update(forms.ModelForm):

    prefix = 'operating_system'

    class Meta:
        model = DeviceOperatingSystem
        fields = [
            "id",
            "version",
            'operating_system_version',
        ]


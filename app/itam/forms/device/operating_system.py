from django import forms
from django.db.models import Q

from app import settings

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'instance' in kwargs.keys():

            if kwargs['instance'] is not None:

                self.fields['_created'] = forms.DateTimeField(
                    label="Install Date",
                    input_formats=settings.DATETIME_FORMAT,
                    initial=kwargs['instance'].installdate,
                    disabled=True
                )


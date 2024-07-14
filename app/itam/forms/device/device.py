from django import forms
from django.db.models import Q

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
            'model_notes',
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(kwargs['instance'], 'inventorydate'):
            self.fields['lastinventory'] = forms.DateTimeField(
                label="Last Inventory Date",
                input_formats=settings.DATETIME_FORMAT,
                initial=kwargs['instance'].inventorydate,
                disabled=True,
                required=False,
            )

        # for key in self.fields.keys():
        #     self.fields[key].widget.attrs['disabled'] = True

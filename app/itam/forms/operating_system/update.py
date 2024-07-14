from django import forms
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm

from itam.models.operating_system import OperatingSystem



class OperatingSystemFormCommon(CommonModelForm):

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



class Update(OperatingSystemFormCommon):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['_created'] = forms.DateTimeField(
            label="Created",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].created,
            disabled=True
        )

        self.fields['_modified'] = forms.DateTimeField(
            label="Modified",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].modified,
            disabled=True
        )


        if kwargs['instance'].is_global:

            self.fields['is_global'].widget.attrs['disabled'] = True

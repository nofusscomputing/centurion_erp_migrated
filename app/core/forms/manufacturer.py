from django import forms

from core.forms.common import CommonModelForm
from core.models.manufacturer import Manufacturer



class ManufacturerForm(CommonModelForm):

    class Meta:

        fields = [
            'name',
            'slug',
            'id',
            'organization',
            'is_global',
            'model_notes',
        ]

        model = Manufacturer

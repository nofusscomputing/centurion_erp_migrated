from django import forms

from core.models.manufacturer import Manufacturer



class ManufacturerForm(forms.ModelForm):

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

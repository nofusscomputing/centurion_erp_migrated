from django import forms

from core.forms.common import CommonModelForm
from core.models.manufacturer import Manufacturer

from settings.forms.admin_settings_global import AdminGlobalModels



class ManufacturerForm(
    AdminGlobalModels,
    CommonModelForm
):

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

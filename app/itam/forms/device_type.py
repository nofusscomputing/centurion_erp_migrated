from django.db.models import Q

from core.forms.common import CommonModelForm

from itam.models.device import DeviceType

from settings.forms.admin_settings_global import AdminGlobalModels



class DeviceTypeForm(
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

       model = DeviceType

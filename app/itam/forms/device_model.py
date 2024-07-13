from django.db.models import Q

from core.forms.common import CommonModelForm

from itam.models.device_models import DeviceModel



class DeviceModelForm(CommonModelForm):

    class Meta:

       fields = [
        'name',
        'slug',
        'manufacturer',
        'id',
        'organization',
        'is_global',
        'model_notes',
       ]

       model = DeviceModel

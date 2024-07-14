from django.db.models import Q

from core.forms.common import CommonModelForm

from itam.models.device import DeviceType



class DeviceTypeForm(CommonModelForm):

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

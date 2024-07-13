from django.db.models import Q

from config_management.models.groups import ConfigGroupSoftware

from core.forms.common import CommonModelForm

from itam.models.software import Software


class SoftwareAdd(CommonModelForm):

    class Meta:
       model = ConfigGroupSoftware
       fields = [
        'software',
        'action'
       ]

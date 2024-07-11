from django.db.models import Q

from config_management.models.groups import ConfigGroups

from core.forms.common import CommonModelForm

from itam.models.software import Software, SoftwareVersion


class ConfigGroupForm(CommonModelForm):

    class Meta:
       model = ConfigGroups
       fields = [
        'name',
        'parent',
        'is_global',
        'config',
       ]

from itam.models.device import Device

from config_management.models.groups import ConfigGroups, ConfigGroupHosts

from core.forms.common import CommonModelForm



class ConfigGroupHostsForm(CommonModelForm):

    __name__ = 'asdsa'

    class Meta:

        fields = [
            'host'
        ]

        model = ConfigGroupHosts

    prefix = 'config_group_hosts'

from django import forms

from itam.models.device import Device

from config_management.models.groups import ConfigGroups, ConfigGroupHosts


class ConfigGroupHostsForm(forms.ModelForm):

    __name__ = 'asdsa'

    class Meta:

        fields = [
            'host'
        ]

        model = ConfigGroupHosts

    prefix = 'config_group_hosts'

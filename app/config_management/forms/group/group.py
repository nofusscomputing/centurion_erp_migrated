from django import forms
from django.db.models import Q

from config_management.models.groups import ConfigGroups
from itam.models.software import Software, SoftwareVersion


class ConfigGroupForm(forms.ModelForm):

    class Meta:
       model = ConfigGroups
       fields = [
        'name',
        'parent',
        'is_global',
        'config',
       ]

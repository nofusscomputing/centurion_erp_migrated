from django import forms
from django.db.models import Q

from itam.models.device import DeviceSoftware
from itam.models.software import Software


class SoftwareAdd(forms.ModelForm):

    class Meta:
       model = DeviceSoftware
       fields = [
        'software',
        'action'
       ]

    def __init__(self, *args, **kwargs):
        organizations = kwargs.pop('organizations')
        super().__init__(*args, **kwargs)

        self.fields['software'].queryset = Software.objects.filter(Q(organization_id__in=organizations) | Q(is_global = True))

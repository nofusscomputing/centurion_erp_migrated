from django import forms
from django.db.models import Q

from itam.models.device import DeviceSoftware
from itam.models.software import Software, SoftwareVersion


class SoftwareUpdate(forms.ModelForm):

    class Meta:
       model = DeviceSoftware
       fields = [
        'action',
        'version',
       ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['version'].queryset = SoftwareVersion.objects.filter(software_id=self.instance.software.id)
        

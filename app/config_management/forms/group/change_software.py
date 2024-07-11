from django.db.models import Q

from config_management.models.groups import ConfigGroupSoftware

from core.forms.common import CommonModelForm

from itam.models.software import Software, SoftwareVersion


class SoftwareUpdate(CommonModelForm):

    class Meta:
       model = ConfigGroupSoftware
       fields = [
        'action',
        'version',
       ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['version'].queryset = SoftwareVersion.objects.filter(software_id=self.instance.software.id)


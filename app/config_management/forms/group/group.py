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
        'organization',
        'model_notes',
        'config',
       ]


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        if hasattr(kwargs['instance'], 'id'):

            self.fields['parent'].queryset = self.fields['parent'].queryset.filter(
            ).exclude(
                id=int(kwargs['instance'].id)
            )

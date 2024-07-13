from django.db.models import Q

from core.forms.common import CommonModelForm

from itam.models.software import Software



class SoftwareForm(CommonModelForm):

    class Meta:
        model = Software
        fields = [
            "name",
            'publisher',
            'slug',
            'id',
            'organization',
            'is_global',
            'category',
            'model_notes',
        ]



class SoftwareFormUpdate(SoftwareForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['is_global'].widget.attrs['disabled'] = True

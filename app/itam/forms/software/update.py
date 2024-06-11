from django import forms
from django.db.models import Q

from itam.models.software import Software


class Update(forms.ModelForm):

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['is_global'].widget.attrs['disabled'] = True

from django import forms
from django.forms import ValidationError
from django.urls import reverse

from itim.models.clusters import ClusterType

from app import settings

from core.forms.common import CommonModelForm



class ClusterTypeForm(CommonModelForm):


    class Meta:

        fields = '__all__'

        model = ClusterType

    prefix = 'cluster_type'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)



class DetailForm(ClusterTypeForm):


    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'organization',
                        'c_created',
                        'c_modified'
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
            ]
        },
        "notes": {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.fields['c_created'] = forms.DateTimeField(
            label = 'Created',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.created,
        )

        self.fields['c_modified'] = forms.DateTimeField(
            label = 'Modified',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.modified,
        )

        self.tabs['details'].update({
            "edit_url": reverse('Settings:_cluster_type_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('Settings:_cluster_types')


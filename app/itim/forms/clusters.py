from django import forms
from django.forms import ValidationError
from django.urls import reverse

from itim.models.clusters import Cluster

from app import settings

from core.forms.common import CommonModelForm



class ClusterForm(CommonModelForm):


    class Meta:

        fields = '__all__'

        model = Cluster

    prefix = 'cluster'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['parent_cluster'].queryset = self.fields['parent_cluster'].queryset.exclude(
            id=self.instance.pk
        )

        self.fields['devices'].queryset = self.fields['devices'].queryset.exclude(
            is_virtual=False
        )


    def clean(self):
        
        cleaned_data = super().clean()

        pk = self.instance.id

        parent_cluster = cleaned_data.get("parent_cluster")

        if pk:

            if parent_cluster == pk:

                raise ValidationError("Cluster can't have itself as its parent cluster")

        return cleaned_data



class DetailForm(ClusterForm):


    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'parent_cluster',
                        'cluster_type',
                        'name',
                        'organization',
                        'c_created',
                        'c_modified'
                    ],
                    "right": [
                        'model_notes',
                        'resources',
                    ]
                },
            ]
        },
        "rendered_config": {
            "name": "Rendered Config",
            "slug": "rendered_config",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        'rendered_config',
                    ],
                    "json": [
                        'rendered_config'
                    ]
                }
            ]
        },
        "tickets": {
            "name": "Tickets",
            "slug": "tickets",
            "sections": []
        },
        "notes": {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        # self.fields['config_variables'] = forms.fields.JSONField(
        #     widget = forms.Textarea(
        #         attrs = {
        #             "cols": "80",
        #             "rows": "100"
        #         }
        #     ),
        #     label = 'Rendered Configuration',
        #     initial = self.instance.config_variables,
        # )

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

        self.fields['resources'] = forms.CharField(
            label = 'Available Resources',
            disabled = True,
            initial = 'xx/yy CPU, xx/yy RAM, xx/yy Storage',
        )


        self.fields['rendered_config'] = forms.fields.JSONField(
            label = 'Available Resources',
            disabled = True,
            initial = self.instance.rendered_config,
        )


        self.tabs['details'].update({
            "edit_url": reverse('ITIM:_cluster_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('ITIM:Clusters')


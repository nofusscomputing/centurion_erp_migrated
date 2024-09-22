from django import forms
from django.forms import ValidationError
from django.urls import reverse

from itim.models.services import Service

from app import settings

from core.forms.common import CommonModelForm



class ServiceForm(CommonModelForm):


    class Meta:

        fields = '__all__'

        model = Service

    prefix = 'service'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['dependent_service'].queryset = self.fields['dependent_service'].queryset.exclude(
            id=self.instance.pk
        ).exclude(
            is_template=True
        )

        self.fields['template'].queryset = self.fields['template'].queryset.exclude(
            id=self.instance.pk
        )


    def clean(self):
        
        cleaned_data = super().clean()

        pk = self.instance.id
        dependent_service = cleaned_data.get("dependent_service")
        device = cleaned_data.get("device")
        cluster = cleaned_data.get("cluster")
        config_key_variable = cleaned_data.get("config_key_variable")
        is_template = cleaned_data.get("is_template")
        template = cleaned_data.get("template")
        port = cleaned_data.get("port")


        if not is_template and not template:

            if not device and not cluster:

                raise ValidationError('A Service must be assigned to either a "Cluster" or a "Device".')


            if device and cluster:

                raise ValidationError('A Service must only be assigned to either a "Cluster" or a "Device". Not both.')


            if not port:

                raise ValidationError('Port(s) must be assigned to a service.')

        if not is_template and not config_key_variable:

            raise ValidationError('Configuration Key must be specified')

        if dependent_service:

            for dependency in dependent_service:

                query = Service.objects.filter(
                    dependent_service = pk,
                    id = dependency.id,
                )

                if query.exists():

                    raise ValidationError('A dependent service already depends upon this service. Circular dependencies are not allowed.')

            


        return cleaned_data



class DetailForm(ServiceForm):


    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'config_key_variable',
                        'template',
                        'organization',
                        'c_created',
                        'c_modified'
                    ],
                    "right": [
                        'model_notes',
                    ]
                }
            ]
        },
        "rendered_config": {
            "name": "Rendered Config",
            "slug": "rendered_config",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        'config_variables',
                    ],
                    "json": [
                        'config_variables'
                    ]
                }
            ]
        },
        "tickets": {
            "name": "Tickets",
            "slug": "tickets",
            "sections": []
        },
    }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.fields['config_variables'] = forms.fields.JSONField(
            widget = forms.Textarea(
                attrs = {
                    "cols": "80",
                    "rows": "100"
                }
            ),
            label = 'Rendered Configuration',
            initial = self.instance.config_variables,
        )

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
            "edit_url": reverse('ITIM:_service_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('ITIM:Services')


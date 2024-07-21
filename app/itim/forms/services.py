from django import forms
from django.forms import ValidationError

from itim.models.services import Service

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

        if dependent_service:

            for dependency in dependent_service:

                query = Service.objects.filter(
                    dependent_service = pk,
                    id = dependency.id,
                )

                if query.exists():

                    raise ValidationError('A dependent service already depends upon this service. Circular dependencies are not allowed.')

            


        return cleaned_data

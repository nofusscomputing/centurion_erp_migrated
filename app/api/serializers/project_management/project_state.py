from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from project_management.models.project_states import ProjectState



class ProjectStateSerializer(
    serializers.ModelSerializer,
):

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_project_state-detail", format="html"
    )


    class Meta:

        model = ProjectState

        fields = '__all__'

        read_only_fields = [
            'id',
            'url',
        ]


    def __init__(self, instance=None, data=empty, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)

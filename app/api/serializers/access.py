from rest_framework import serializers
from access.models import Organization, Team


class TeamSerializer(serializers.ModelSerializer):


    class Meta:
        model = Team
        fields = (
            "group_ptr_id",
            "name",
        )



class OrganizationSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="_api_organization", format="html"
    )


    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            'url',
        )

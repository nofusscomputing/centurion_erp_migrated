from rest_framework import serializers
from itam.models.device import Software




class SoftwareSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_software_view", format="html"
    )

    class Meta:
        model = Software
        fields = '__all__'

        read_only_fields = [
            'slug',
        ]
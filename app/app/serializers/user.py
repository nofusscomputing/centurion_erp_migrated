from django.contrib.auth.models import User

from rest_framework import serializers



class UserBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )


    class Meta:

        model = User

        fields = '__all__'

        fields = [
            'id',
            'display_name',
            'first_name',
            'last_name',
            'username',
            'is_active',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'first_name',
            'last_name',
            'username',
            'is_active',
        ]

from django import forms

from settings.models.user_settings import UserSettings


class UserSettingsForm(forms.ModelForm):

    prefix = 'user_settings'

    class Meta:

        fields = [
            'default_organization',
        ]

        model = UserSettings

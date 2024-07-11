from django import forms
from django.db.models import Q

from django.contrib.auth.models import User

from access.models import Organization, TeamUsers

from core.forms.common import CommonModelForm

from settings.models.user_settings import UserSettings


class UserSettingsForm(CommonModelForm):

    prefix = 'user_settings'

    class Meta:

        fields = [
            'default_organization',
        ]

        model = UserSettings


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        user_organizations = []

        for team_user in TeamUsers.objects.filter(user=kwargs['instance'].user):

            if team_user.team.organization.name not in user_organizations:

                user_organizations += [ team_user.team.organization.name ]


        self.fields['default_organization'].queryset = Organization.objects.filter(
            Q(name__in=user_organizations)
            |
            Q(manager=kwargs['instance'].user)
        )

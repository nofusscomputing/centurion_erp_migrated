from django import forms

from django.db.models import Q

from access.models import Organization, TeamUsers



class CommonModelForm(forms.ModelForm):

    _organizations = None

    organization_field: str = 'organization'


    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        user_organizations: list([str]) = []

        for team_user in TeamUsers.objects.filter(user=user):

            if team_user.team.organization.name not in user_organizations:

                if not user_organizations:

                    self.user_organizations = []

                user_organizations += [ team_user.team.organization.name ]

        if user_organizations:

            self._organizations = Organization.objects.filter(
                Q(name__in=user_organizations)
                |
                Q(manager=user)
            )

        new_kwargs: dict = {}

        for key, value in kwargs.items():

            if key != 'user':

                new_kwargs.update({key: value})

        super().__init__(*args, **new_kwargs)

        if self.Meta.fields:

            if self.organization_field in self.Meta.fields:

                self.fields[self.organization_field].queryset = self._organizations

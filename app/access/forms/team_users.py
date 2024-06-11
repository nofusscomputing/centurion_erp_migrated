from django import forms
from django.db.models import Q

from app import settings

from access.models import TeamUsers


class TeamUsersForm(forms.ModelForm):

    class Meta:
        model = TeamUsers
        fields = [
            'user',
            'manager',
        ]

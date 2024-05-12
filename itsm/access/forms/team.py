from django import forms

from django.forms import BaseInlineFormSet, BaseModelFormSet, ModelForm

from access.models import Organization, Team

from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple


class TeamForm(BaseInlineFormSet):

    model = Team

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Team.objects.filter(pk=team_id)

from django import forms
from django.db.models import Q

from django.contrib.auth.models import User

from access.models import Organization, TeamUsers

from core.forms.common import CommonModelForm

from settings.models.app_settings import AppSettings


class AppSettingsForm(CommonModelForm):

    class Meta:

        fields = AppSettings.__all__

        model = AppSettings

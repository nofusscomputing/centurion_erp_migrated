from django import forms
from django.db.models import Q

from django.contrib.auth.models import User

from access.models import Organization, TeamUsers

from core.forms.common import CommonModelForm

from settings.models.external_link import ExternalLink


class ExternalLinksForm(CommonModelForm):

    prefix = 'external_links'

    class Meta:

        fields = '__all__'

        model = ExternalLink

from django import forms
from django.db.models import Q

from django.contrib.auth.models import User

from access.models import Organization, TeamUsers

from core.forms.common import CommonModelForm

from settings.models.app_settings import AppSettings


class AdminGlobalModels:
    """Administratively set Global Models
    
    Use this class on models that can be set within the application settings as a global
    application.
    """


    def __init__(self, *args, **kwargs):
        """ Init Form
        
        As these forms are for administratively set global organization, set the `organization` and `is_global` fields
        to be read only.
        """

        super().__init__(*args, **kwargs)

        self.fields['organization'].widget.attrs['readonly'] = True
        self.fields['is_global'].widget.attrs['readonly'] = True

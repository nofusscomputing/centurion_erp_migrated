
# from django import forms
# from django.forms import ValidationError

# from app import settings

from itim.models.services import Port

from core.forms.common import CommonModelForm

from settings.models.user_settings import UserSettings



class PortForm(CommonModelForm):


    class Meta:

        fields = '__all__'

        model = Port

    prefix = 'port'

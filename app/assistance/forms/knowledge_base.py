
from django import forms
from django.forms import ValidationError

from app import settings

from assistance.models.knowledge_base import KnowledgeBase

from core.forms.common import CommonModelForm



class KnowledgeBaseForm(CommonModelForm):

    __name__ = 'asdsa'

    class Meta:

        fields = '__all__'

        model = KnowledgeBase

    prefix = 'knowledgebase'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['expiry_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'format': "%Y-%m-%dT%H:%M"})
        self.fields['expiry_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['expiry_date'].format="%Y-%m-%dT%H:%M"

        self.fields['release_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'format': "%Y-%m-%dT%H:%M"})
        self.fields['release_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['release_date'].format="%Y-%m-%dT%H:%M"


    def clean(self):
        
        cleaned_data = super().clean()

        responsible_user = cleaned_data.get("responsible_user")
        responsible_teams = cleaned_data.get("responsible_teams")


        if not responsible_user and not responsible_teams:

            raise ValidationError('A Responsible User or Team must be assigned.')


        target_team = cleaned_data.get("target_team")
        target_user = cleaned_data.get("target_user")


        if not target_team and not target_user:

            raise ValidationError('A Target Team or Target User must be assigned.')


        if target_team and target_user:

            raise ValidationError('Both a Target Team or Target User Cant be assigned at the same time. Use one or the other')


        return cleaned_data

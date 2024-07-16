from django import forms
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm

from project_management.models.projects import Project



class ProjectForm(CommonModelForm):

    prefix = 'project'

    class Meta:
        fields = '__all__'


        model = Project


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['planned_start_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'format': "%Y-%m-%dT%H:%M"})
        self.fields['planned_start_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['planned_start_date'].format="%Y-%m-%dT%H:%M"

        self.fields['planned_finish_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['planned_finish_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['planned_finish_date'].format="%Y-%m-%dT%H:%M"

        self.fields['real_start_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['real_start_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['real_start_date'].format="%Y-%m-%dT%H:%M"

        self.fields['real_finish_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['real_finish_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['real_finish_date'].format="%Y-%m-%dT%H:%M"

        self.fields['description'].widget.attrs = {'style': "height: 800px; width: 1000px"}


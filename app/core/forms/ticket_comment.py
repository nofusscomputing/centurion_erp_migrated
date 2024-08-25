from django import forms
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm

from core.models.ticket.ticket_comment import TicketComment


class CommentForm(CommonModelForm):

    prefix = 'ticket'

    class Meta:
        model = TicketComment
        fields = '__all__'


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

        self.fields['body'].widget.attrs = {'style': "height: 800px; width: 900px"}

        self.fields['user'].initial = kwargs['user'].pk
        self.fields['user'].widget = self.fields['user'].hidden_widget()

        self.fields['ticket'].widget = self.fields['ticket'].hidden_widget()

        if 'qs_comment_type' in kwargs['initial']:

            comment_type = kwargs['initial']['qs_comment_type']

        else:

            comment_type = str(self.instance.get_comment_type_display()).lower()


        original_fields = self.fields.copy()
        comment_fields = []


        if (
            kwargs['initial']['type_ticket'] == 'request'
                or
            kwargs['initial']['type_ticket'] == 'incident'
                or
            kwargs['initial']['type_ticket'] == 'problem'
                or
            kwargs['initial']['type_ticket'] == 'change'
                or
            kwargs['initial']['type_ticket'] == 'project_task'
        ):

            if comment_type == 'task':

                comment_fields = self.Meta.model.fields_itsm_task

                self.fields['comment_type'].initial = self.Meta.model.CommentType.TASK

            elif comment_type == 'comment':

                comment_fields = self.Meta.model.common_itsm_fields

                self.fields['comment_type'].initial = self.Meta.model.CommentType.COMMENT


            elif comment_type == 'solution':

                comment_fields = self.Meta.model.common_itsm_fields

                self.fields['comment_type'].initial = self.Meta.model.CommentType.SOLUTION

            elif comment_type == 'notification':

                comment_fields = self.Meta.model.fields_itsm_notification

                self.fields['comment_type'].initial = self.Meta.model.CommentType.NOTIFICATION

        elif kwargs['initial']['type_ticket'] == 'issue':

            comment_fields = self.Meta.model.fields_git_issue

        elif kwargs['initial']['type_ticket'] == 'merge':

            comment_fields = self.Meta.model.fields_git_merge


        for field in original_fields:

            if field not in comment_fields:

                del self.fields[field]

    def clean(self):
        
        cleaned_data = super().clean()

        return cleaned_data

    def is_valid(self) -> bool:

        is_valid = super().is_valid()

        return is_valid



class DetailForm(CommentForm):

    prefix = 'ticket'

    class Meta:
        model = TicketComment
        fields = '__all__'


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

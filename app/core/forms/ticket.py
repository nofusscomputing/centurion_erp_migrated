from django import forms
from django.db.models import Q
from django.forms import ValidationError

from app import settings

from core.forms.common import CommonModelForm
from core.forms.validate_ticket import TicketValidation

from core.models.ticket.ticket import Ticket, RelatedTickets



class TicketForm(
    CommonModelForm,
    TicketValidation,
):


    class Meta:
        model = Ticket
        fields = '__all__'


    def __init__(self, request, *args, **kwargs):

        self.request = request

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

        self.fields['description'].widget.attrs = {'style': "height: 800px; width: 900px"}

        self.fields['opened_by'].initial = kwargs['user'].pk
        self.fields['opened_by'].widget = self.fields['opened_by'].hidden_widget()

        self.fields['ticket_type'].widget = self.fields['ticket_type'].hidden_widget()

        self.fields['organization'].initial = self.initial['organization']

        if self.instance.pk is not None:
            
            self.fields['organization'].widget = self.fields['organization'].hidden_widget()

        if self.instance.project is not None:

            self.fields['milestone'].queryset = self.fields['milestone'].queryset.filter(
                    project=self.instance.project
                )

        else:

            self.fields['milestone'].queryset = self.fields['milestone'].queryset.filter(
                    id=0
                )


        original_fields = self.fields.copy()
        ticket_type = []

        if kwargs['initial']['type_ticket'] == 'request':

            ticket_type = self.Meta.model.fields_itsm_request

            self.fields['status'].choices = self.Meta.model.TicketStatus.Request

            self.fields['ticket_type'].initial = '1'

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                request=True
            )

        elif kwargs['initial']['type_ticket'] == 'incident':

            ticket_type = self.Meta.model.fields_itsm_incident

            self.fields['status'].choices = self.Meta.model.TicketStatus.Incident

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.INCIDENT.value

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                incident=True
            )

        elif kwargs['initial']['type_ticket'] == 'problem':

            ticket_type = self.Meta.model.fields_itsm_problem

            self.fields['status'].choices = self.Meta.model.TicketStatus.Problem

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.PROBLEM.value

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                problem=True
            )
        elif kwargs['initial']['type_ticket'] == 'change':

            ticket_type = self.Meta.model.fields_itsm_change

            self.fields['status'].choices = self.Meta.model.TicketStatus.Change

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.CHANGE.value

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                change=True
            )
        elif kwargs['initial']['type_ticket'] == 'issue':

            ticket_type = self.Meta.model.fields_git_issue

            self.fields['status'].choices = self.Meta.model.TicketStatus.Git

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.ISSUE.value

        elif kwargs['initial']['type_ticket'] == 'merge':

            ticket_type = self.Meta.model.fields_git_merge

            self.fields['status'].choices = self.Meta.model.TicketStatus.Git

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.MERGE_REQUEST.value

        elif kwargs['initial']['type_ticket'] == 'project_task':

            ticket_type = self.Meta.model.fields_project_task

            self.fields['status'].choices = self.Meta.model.TicketStatus.ProjectTask

            self._project: int = kwargs['initial']['project']

            self.fields['project'].initial = self._project
            self.fields['project'].widget = self.fields['project'].hidden_widget()

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.PROJECT_TASK.value

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                project_task=True
            )

        if kwargs['user'].is_superuser:

            ticket_type += self.Meta.model.tech_fields

        self.ticket_type_fields = ticket_type

        fields_allowed_by_permission = self.get_fields_allowed_by_permission

        allowed_ticket_fields: list = []

        for field in fields_allowed_by_permission:    # Remove fields not intended for the ticket type


            if field in ticket_type:
                
                allowed_ticket_fields = allowed_ticket_fields + [ field ]


        for field in original_fields:    # Remove fields user cant edit unless field is hidden

            if (
                (
                    field not in allowed_ticket_fields and not self.fields[field].widget.is_hidden
                )
                    or
                field not in ticket_type
            ):

                # self.fields[field].widget = self.fields[field].hidden_widget()
                del self.fields[field]


    def clean(self):
        
        cleaned_data = super().clean()

        return cleaned_data


    def is_valid(self) -> bool:

        is_valid = super().is_valid()

        self.validate_ticket()

        if self._ticket_type == 'change':

            self.validate_change_ticket()

        elif self._ticket_type == 'incident':

            self.validate_incident_ticket()

        elif self._ticket_type == 'issue':

            # self.validate_issue_ticket()
            raise ValidationError(
                'This Ticket type is not yet available'
            )

        elif self._ticket_type == 'merge_request':

            # self.validate_merge_request_ticket()
            raise ValidationError(
                'This Ticket type is not yet available'
            )

        elif self._ticket_type == 'problem':

            self.validate_problem_ticket()

        elif self._ticket_type == 'project_task':

            self.validate_project_task_ticket()

        elif self._ticket_type == 'request':

            self.validate_request_ticket()

        else:

            raise ValidationError('Ticket Type must be set')


        return is_valid



class DetailForm(CommonModelForm):

    prefix = 'ticket'

    class Meta:
        model = Ticket
        fields = '__all__'

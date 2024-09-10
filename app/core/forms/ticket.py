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
        self.fields['organization'].widget = self.fields['organization'].hidden_widget()


        original_fields = self.fields.copy()
        ticket_type = []

        if kwargs['initial']['type_ticket'] == 'request':

            ticket_type = self.Meta.model.fields_itsm_request

            self.fields['status'].choices = self.Meta.model.TicketStatus.Request

            self.fields['ticket_type'].initial = '1'

        elif kwargs['initial']['type_ticket'] == 'incident':

            ticket_type = self.Meta.model.fields_itsm_incident

            self.fields['status'].choices = self.Meta.model.TicketStatus.Incident

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.INCIDENT.value

        elif kwargs['initial']['type_ticket'] == 'problem':

            ticket_type = self.Meta.model.fields_itsm_problem

            self.fields['status'].choices = self.Meta.model.TicketStatus.Problem

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.PROBLEM.value

        elif kwargs['initial']['type_ticket'] == 'change':

            ticket_type = self.Meta.model.fields_itsm_change

            self.fields['status'].choices = self.Meta.model.TicketStatus.Change

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.CHANGE.value

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

            self.fields['ticket_type'].initial = self.Meta.model.TicketType.PROJECT_TASK.value

        # self.fields['status'].widget = self.fields['status'].hidden_widget()

        if kwargs['user'].is_superuser:

            ticket_type += self.Meta.model.tech_fields

        fields_allowed = self.fields_allowed


        for field in fields_allowed:    # Remove fields not intended for the ticket type

            if field not in ticket_type:

                self._fields_allowed.remove(field)


        for field in original_fields:    # Remove fields user cant edit unless field is hidden

            if (
                (
                    field not in self._fields_allowed and not self.fields[field].widget.is_hidden
                )
                    or
                field not in ticket_type
            ):

                del self.fields[field]


    def clean(self):
        
        cleaned_data = super().clean()

        return cleaned_data


    def is_valid(self) -> bool:

        is_valid = super().is_valid()

        if self.instance.pk:
        
            self.original_object = self.Meta.model.objects.get(pk=self.instance.pk)

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

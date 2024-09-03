from django.core.exceptions import PermissionDenied
from django.forms import ValidationError

from rest_framework import serializers

from access.mixin import OrganizationMixin


class TicketValidation(
    OrganizationMixin,
):
    """Ticket Form/Serializer Validation

    Validate a ticket form or api viewset

    Raises:
        PermissionDenied: User has no allowable fields to edit
        PermissionDenied: User is lacking permission to edit a field
        serializers.ValidationError: Status field has a value set that does not meet the ticket type
        ValidationError: Status field has a value set that does not meet the ticket type

    """

    original_object = None

    add_fields: list = [
        'title',
        'description',
        'urgency',
    ]

    change_fields: list = []

    delete_fields: list = [
        'is_deleted',
    ]

    import_fields: list = [
        'assigned_users',
        'assigned_teams',
        'created',
        'date_closed',
        'external_ref',
        'external_system',
        'status',
        'impact',
        'opened_by',
        'planned_start_date',
        'planned_finish_date',
        'priority',
        'project',
        'real_start_date',
        'real_finish_date',
        'subscribed_users',
        'subscribed_teams',
        'ticket_type',
    ]

    triage_fields: list = [
        'assigned_users',
        'assigned_teams',
        'status',
        'impact',
        'opened_by',
        'planned_start_date',
        'planned_finish_date',
        'priority',
        'project',
        'real_start_date',
        'real_finish_date',
        'subscribed_users',
        'subscribed_teams',
    ]

    @property
    def fields_allowed(self):

        if not hasattr(self, '_ticket_type'):
            
            self._ticket_type = self.initial['type_ticket']


        fields_allowed: list = []

        if self.instance is not None:

            ticket_organization = self.instance.organization

        else:

            ticket_organization = self.validated_data['organization']


        if ticket_organization is None:

            ticket_organization = self.initial['organization']


        if self.has_organization_permission(
            organization=ticket_organization.id,
            permissions_required = [ 'core.add_ticket_'+ self._ticket_type ],
        ) and not self.request.user.is_superuser:

            fields_allowed = self.add_fields


        if self.has_organization_permission(
            organization=ticket_organization.id,
            permissions_required = [ 'core.change_ticket_'+ self._ticket_type ],
        ) and not self.request.user.is_superuser:

            if len(fields_allowed) == 0:

                fields_allowed = self.add_fields + self.change_fields

            else:

                fields_allowed = fields_allowed + self.change_fields

        if self.has_organization_permission(
            organization=ticket_organization.id,
            permissions_required = [ 'core.delete_ticket_'+ self._ticket_type ],
        ) and not self.request.user.is_superuser:

            fields_allowed = fields_allowed + self.delete_fields

        if self.has_organization_permission(
            organization=ticket_organization.id,
            permissions_required = [ 'core.import_ticket_'+ self._ticket_type ],
        ) and not self.request.user.is_superuser:

            fields_allowed = fields_allowed + self.import_fields

        if self.has_organization_permission(
            organization=ticket_organization.id,
            permissions_required = [ 'core.triage_ticket_'+ self._ticket_type ],
        ) and not self.request.user.is_superuser:

            fields_allowed = fields_allowed + self.triage_fields

        if self.request.user.is_superuser:

            all_fields: list = self.add_fields
            all_fields = all_fields + self.change_fields
            all_fields = all_fields + self.delete_fields
            all_fields = all_fields + self.import_fields
            all_fields = all_fields + self.triage_fields

            fields_allowed = fields_allowed + all_fields

        return fields_allowed


    def validate_field_permission(self):
        """ Check field permissions

        Users can't edit all fields. They can only adjust fields that they
        have the permissions to adjust.

        Raises:
            PermissionDenied: Access Denied when user has no ticket permissions assigned
            PermissionDenied: User tried to edit a field they dont have permission to edit.
        """

        fields_allowed = self.fields_allowed

        if len(fields_allowed) == 0:

            raise PermissionDenied('Access Denied')

        for field in self.changed_data:

            if field not in fields_allowed and not self.fields['status'].widget.is_hidden:

                raise PermissionDenied(f'cant edit field: {field}')



    def validate_field_status(self):
        """Validate status field

        Ticket status depends upon ticket type.
        Ensure that the corrent status is used.
        """

        is_valid = False

        if not hasattr(self, '_ticket_type'):
            
            self._ticket_type = self.initial['type_ticket']


        if hasattr(self, 'cleaned_data'):

            field = self.cleaned_data['status']

        else:

            field = self.validated_data['status']


        if self._ticket_type == 'request':

            if field in self.Meta.model.TicketStatus.Request._value2member_map_:

                is_valid = True

        elif self._ticket_type == 'incident':

            if field in self.Meta.model.TicketStatus.Incident._value2member_map_:

                is_valid = True

        elif self._ticket_type == 'problem':

            if field in self.Meta.model.TicketStatus.Problem._value2member_map_:

                is_valid = True

        elif self._ticket_type == 'change':

            if field in self.Meta.model.TicketStatus.Change._value2member_map_:

                is_valid = True

        elif self._ticket_type == 'issue':

            if field in self.Meta.model.TicketStatus.Issue._value2member_map_:

                is_valid = True

        elif self._ticket_type == 'merge':

            if field in self.Meta.model.TicketStatus.Merge._value2member_map_:

                is_valid = True

        elif self._ticket_type == 'project_task':

            if field in self.Meta.model.TicketStatus.ProjectTask._value2member_map_:

                is_valid = True

        
        if not is_valid:

            if hasattr(self, 'validated_data'):

                raise serializers.ValidationError('Incorrect Status set')

            else:

                raise ValidationError('Incorrect Status set')

        
        return is_valid


    def validate_ticket(self):
        """Validations common to all ticket types."""

        is_valid = False

        if hasattr(self, 'validated_data'):

            changed_data: list = []

            changed_data_exempt = [
                'ticket_comments',
                'url',
            ]

            for field in self.validated_data:

                if field in changed_data_exempt:
                    continue

                if self.original_object is not None:
                    if (
                        self.validated_data[field] != getattr(self.original_object, field)
                        and (
                            type(self.validated_data[field]) in [str, int, bool]
                        )
                    ) :

                        changed_data = changed_data + [ field ]
                else:


                    if type(self.validated_data[field]) in [str, int, bool]:

                        changed_data = changed_data + [ field ]

            if len(changed_data) > 0:

                self.changed_data = changed_data

        validate_field_permission = False
        if self.validate_field_permission():

            validate_field_permission = True


        validate_field_status = False
        if self.validate_field_status():

            validate_field_status = True

        if validate_field_permission and validate_field_status:
            is_valid = True

        return is_valid



    def validate_change_ticket(self):

        # check status

        # check type

        pass


    def validate_incident_ticket(self):

        # check status

        # check type

        pass


    def validate_problem_ticket(self):

        # check status

        # check type

        pass


    def validate_request_ticket(self):

        # check status

        # check type

        # raise ValidationError('Test to see what it looks like')
        pass

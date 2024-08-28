from django.core.exceptions import PermissionDenied
from django.forms import ValidationError

from access.mixin import OrganizationMixin


class TicketValidation(
    OrganizationMixin,
):

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

    triage_fields: list = [
        'assigned_users',
        'assigned_teams',
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


        fields_allowed: list = []


        if self.has_organization_permission(
            organization=self.instance.organization.id,
            permissions_required = [ 'core.add_ticket_'+ self.initial['type_ticket'] ],
        ) and not self.request.user.is_superuser:

            fields_allowed = self.add_fields


        if self.has_organization_permission(
            organization=self.instance.organization.id,
            permissions_required = [ 'core.change_ticket_'+ self.initial['type_ticket'] ],
        ) and not self.request.user.is_superuser:

            if len(fields_allowed) == 0:

                fields_allowed = self.add_fields + self.change_fields

            else:

                fields_allowed = fields_allowed + self.change_fields

        if self.has_organization_permission(
            organization=self.instance.organization.id,
            permissions_required = [ 'core.delete_ticket_'+ self.initial['type_ticket'] ],
        ) and not self.request.user.is_superuser:

            fields_allowed = fields_allowed + self.delete_fields

        if self.has_organization_permission(
            organization=self.instance.organization.id,
            permissions_required = [ 'core.import_ticket_'+ self.initial['type_ticket'] ],
        ) and not self.request.user.is_superuser:

            fields_allowed = fields_allowed + self.import_fields

        if self.has_organization_permission(
            organization=self.instance.organization.id,
            permissions_required = [ 'core.triage_ticket_'+ self.initial['type_ticket'] ],
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
            PermissionDenied: _description_
        """

        fields_allowed = self.fields_allowed

        if len(fields_allowed) == 0:

            raise PermissionDenied('Access Denied')

        for field in self.changed_data:

            if field not in fields_allowed:

                raise PermissionDenied(f'cant edit field: {field}')



    def validate_ticket(self):
        """Validations common to all ticket types."""

        self.validate_field_permission()



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

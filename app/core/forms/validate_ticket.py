from django.core.exceptions import PermissionDenied, ValidationError

from rest_framework import serializers

from access.mixin import OrganizationMixin


class TicketValidation(
    OrganizationMixin,
):
    """Ticket Form/Serializer Validation

    Validate a ticket form or api viewset

    ## Class requirements

    - attribute `ticket_type_fields` is set to a list of fields for the ticket type

    - attribute `ticket_type` is set to a string value (lowercase) of the ticket type

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
        'organization'
    ]

    change_fields: list = []

    delete_fields: list = [
        'is_deleted',
    ]

    import_fields: list = [
        'assigned_users',
        'assigned_teams',
        'category',
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
        'milestone',
        'real_start_date',
        'real_finish_date',
        'subscribed_users',
        'subscribed_teams',
        'ticket_type',
    ]

    triage_fields: list = [
        'category',
        'assigned_users',
        'assigned_teams',
        'status',
        'impact',
        'opened_by',
        'planned_start_date',
        'planned_finish_date',
        'priority',
        'project',
        'milestone',
        'real_start_date',
        'real_finish_date',
        'subscribed_users',
        'subscribed_teams',
    ]

    @property
    def get_fields_allowed_by_permission(self):

        if hasattr(self, '_fields_allowed_by_permission'):

            return self._fields_allowed_by_permission

        if not hasattr(self, '_ticket_type'):
            
            self._ticket_type = self.initial['type_ticket']


        fields_allowed: list = []

        if self.instance is not None:

            ticket_organization = self.instance.organization

        else:

            ticket_organization = self.validated_data['organization']


        if ticket_organization is None:

            ticket_organization = self.initial['organization']

        if ticket_organization is None:

            if 'organization' in self.data:

                ticket_organization = self.fields['organization'].queryset.model.objects.get(pk=self.data['organization'])


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

            if hasattr(self, 'serializer_choice_field'):

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

        self._fields_allowed_by_permission = fields_allowed

        return fields_allowed


    @property
    def get_user_changed_fields(self) -> list(str()):
        """List of fields the user changed.

        This data is sourced from the HTTP/POST data.

        Returns:
            list: All of the fields that have changed.
        """

        if hasattr(self, '_user_changed_fields'):

            return self._user_changed_fields

        changed_data: list = []

        changed_data_exempt = [
            '_state',
            'csrfmiddlewaretoken',
            'ticket_comments',
            'url',
        ]

        post_data: dict = self.request.POST.dict().copy()

        for field in post_data:

            if field in self.fields:

                changed_data = changed_data + [ field ]


        if len(changed_data) > 0:

            self._user_changed_fields = changed_data

        return changed_data


    @property
    def validate_field_permission(self):
        """ Check field permissions

        Users can't edit all fields. They can only adjust fields that they
        have the permissions to adjust.

        ## Required fields

        A field marked as required when the instance has no pk, the field will have
        it's permission marked as allowed. This is not the case for items thaat are being
        edited, i.e. have a pk.

        Raises:
            ValidationError: Access Denied when user has no ticket permissions assigned
            ValidationError: User tried to edit a field they dont have permission to edit.
        """

        fields_allowed = self.get_fields_allowed_by_permission

        if len(fields_allowed) == 0:

            raise ValidationError('Access Denied to all fields', code='access_denied_all_fields')


        for field in self.get_user_changed_fields:

            allowed: bool = False

            if (
                field in self.fields
                and field in self.ticket_type_fields
                and (
                    field in fields_allowed
                )
            ):

                allowed = True

            if hasattr(self.instance, 'pk'):

                if (
                    field in self.fields
                    and field in self.ticket_type_fields
                    and self.instance.pk is None
                ):

                    if self.fields[field].required:

                        allowed = True

            elif self.instance is None:

                    if self.fields[field].required:

                        allowed = True


            if not allowed:

                if (
                    self.field_edited(field)
                    or (
                        field not in fields_allowed
                        and field in self.fields
                    )
                ):

                    raise ValidationError(
                        f'cant edit field: {field}',
                        code=f'cant_edit_field_{field}',
                    )

                    return False


        return True


    def field_edited(self, field:str) -> bool:

        if hasattr(self, 'cleaned_data'):    # initial avail in ui

            initial_data: dict = self.initial
            changed_data: dict = self.cleaned_data

        elif hasattr(self, 'validated_data'):    # API

            initial_data:dict = self.instance.__dict__
            changed_data: dict = self.validated_data

        if field in initial_data:

            value = initial_data[field]

        elif str(field) + '_id' in initial_data:

            value = initial_data[str(field) + '_id']

        else:

            return True


        if field in changed_data:

            if changed_data[field] == value:

                return False

            if hasattr(changed_data[field], 'id'):

                if value is None:

                    return True

                if int(value) == changed_data[field].id:

                    return False

            else:

                val = value

                if value is None:

                    return True

                if type(changed_data[field]) is int:

                    val = int(value)

                elif type(changed_data[field]) is bool:

                    val = bool(value)

                elif type(changed_data[field]) is str:

                    val = str(value)


                if val == changed_data[field]:

                    return False

        return True


    def validate_field_milestone(self):

        is_valid: bool = True


        return is_valid


    def validate_field_organization(self) -> bool:
        """Check `organization field`

        Raises:
            ValidationError: user tried to change the organization

        Returns:
            True (bool): OK
            False (bool): User tried to edit the organization
        """

        is_valid: bool = True

        if self.instance is not None:

            if self.instance.pk is not None:

                if 'organization' in self.get_user_changed_fields:

                    if self.field_edited('organization'):

                        is_valid = False

                        raise ValidationError(
                            f'cant edit field: organization',
                            code=f'cant_edit_field_organization',
                        )


        return is_valid


    def validate_field_status(self):
        """Validate status field

        Ticket status depends upon ticket type.
        Ensure that the corrent status is used.
        """

        is_valid = False

        if not hasattr(self, '_ticket_type'):
            
            self._ticket_type = self.initial['type_ticket']

        try:

            if hasattr(self, 'cleaned_data'):

                field = self.cleaned_data['status']

            else:

                field = self.validated_data['status']

        except KeyError:

            # field = self.fields['status'].default.value
            field = getattr(self.Meta.model, 'status').field.default.value


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

        fields: list = []

        if hasattr(self, 'validated_data'):

            fields = self.validated_data

        else:

            fields = self.cleaned_data

        validate_field_permission = False
        if self.validate_field_permission:

            validate_field_permission = True

        validate_field_organization: bool = False
        if self.validate_field_organization():

            validate_field_organization = True


        validate_field_status = False
        if self.validate_field_status():

            validate_field_status = True

        if validate_field_permission and validate_field_status and validate_field_organization:
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

    def validate_project_task_ticket(self):

        if hasattr(self,'_project'):
            self.cleaned_data.update({
                'project': self._project
            })
        
        if self.cleaned_data['project'] is None:

            raise ValidationError('A project task requires a project')

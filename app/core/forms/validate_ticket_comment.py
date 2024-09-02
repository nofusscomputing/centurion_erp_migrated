from django.core.exceptions import PermissionDenied
from django.forms import ValidationError

from rest_framework import serializers

from access.mixin import OrganizationMixin


class TicketCommentValidation(
    OrganizationMixin,
):


    original_object = None

    _comment_type:str = None
    """Human readable comment type. i.e. `request` in lowercase"""

    _ticket_organization = None
    """Ticket Organization as a organization object"""

    _ticket_type: str = None
    """Human readable type of ticket. i.e. `request` in lowercase"""

    add_fields: list = [
        'body',
        'duration'
    ]

    change_fields: list = [
        'body',
    ]

    delete_fields: list = [
        'is_deleted',
    ]

    import_fields: list = [
        'organization',
        'parent',
        'ticket',
        'external_ref',
        'external_system',
        'comment_type',
        'body',
        'created',
        'modified',
        'private',
        'duration',
        'template',
        'is_template',
        'source',
        'status',
        'responsible_user',
        'responsible_team',
        'user',
        'date_closed',
        'planned_start_date',
        'planned_finish_date',
        'real_start_date',
        'real_finish_date',
    ]

    triage_fields: list = [
        'body',
        'private',
        'duration',
        'template',
        'is_template',
        'source',
        'status',
        'responsible_user',
        'responsible_team',
        'planned_start_date',
        'planned_finish_date',
        'real_start_date',
        'real_finish_date',
    ]


    @property
    def fields_allowed(self) -> list(str()):
        """ Get the allowed fields for a ticket ccomment

        Returns:
            list(str): A list of allowed fields for the user
        """

        fields_allowed: list = []


        if self.has_organization_permission(
            organization=self._ticket_organization.id,
            permissions_required = [ 'core.add_ticket_'+ self._ticket_type ],
        ) and not self.request.user.is_superuser:

            fields_allowed = self.add_fields


        if self.has_organization_permission(
            organization=self._ticket_organization.id,
            permissions_required = [ 'core.change_ticketcomment' ],
        ) and not self.request.user.is_superuser:

            if len(fields_allowed) == 0:

                fields_allowed = self.add_fields + self.change_fields

            else:

                fields_allowed = fields_allowed + self.change_fields

        if self.has_organization_permission(
            organization=self._ticket_organization.id,
            permissions_required = [ 'core.delete_ticketcomment' ],
        ) and not self.request.user.is_superuser:

            fields_allowed = fields_allowed + self.delete_fields

        if self.has_organization_permission(
            organization=self._ticket_organization.id,
            permissions_required = [ 'core.import_ticketcomment' ],
        ) and not self.request.user.is_superuser:

            fields_allowed = fields_allowed + self.import_fields

        if self.has_organization_permission(
            organization=self._ticket_organization.id,
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

        comment_fields = []


        if (
            self._ticket_type == 'request'
                or
            self._ticket_type == 'incident'
                or
            self._ticket_type == 'problem'
                or
            self._ticket_type == 'change'
                or
            self._ticket_type == 'project_task'
        ):

            if self._comment_type == 'task':

                comment_fields = self.Meta.model.fields_itsm_task

                self.fields['comment_type'].initial = self.Meta.model.CommentType.TASK

            elif self._comment_type == 'comment':

                comment_fields = self.Meta.model.common_itsm_fields

                self.fields['comment_type'].initial = self.Meta.model.CommentType.COMMENT


            elif self._comment_type == 'solution':

                comment_fields = self.Meta.model.common_itsm_fields

                self.fields['comment_type'].initial = self.Meta.model.CommentType.SOLUTION

            elif self._comment_type == 'notification':

                comment_fields = self.Meta.model.fields_itsm_notification

                self.fields['comment_type'].initial = self.Meta.model.CommentType.NOTIFICATION

        elif self._ticket_type == 'issue':

            comment_fields = self.Meta.model.fields_git_issue

        elif self._ticket_type == 'merge':

            comment_fields = self.Meta.model.fields_git_merge

        
        for comment_field in comment_fields:

            if comment_field not in fields_allowed:

                comment_fields.remove(comment_field)

        return comment_fields




    def validate_field_permission(self):
        pass



    def validate_ticket_comment(self):

        pass

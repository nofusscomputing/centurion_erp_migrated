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

    _ticket_type: str = None
    """Human readable type of ticket. i.e. `request` in lowercase"""


    @property
    def fields_allowed(self):

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

        return comment_fields




    def validate_field_permission(self):
        pass



    def validate_ticket_comment(self):

        pass

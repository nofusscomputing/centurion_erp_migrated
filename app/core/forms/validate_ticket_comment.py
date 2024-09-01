from django.core.exceptions import PermissionDenied
from django.forms import ValidationError

from rest_framework import serializers

from access.mixin import OrganizationMixin


class TicketCommentValidation(
    OrganizationMixin,
):


    original_object = None

    @property
    def fields_allowed(self):

        pass


    def validate_field_permission(self):
        pass



    def validate_ticket_comment(self):

        pass

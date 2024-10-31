from rest_framework import exceptions, status
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied
)

class MissingAttribute(Exception):
    """ An attribute is missing"""

    pass

class APIError(
    exceptions.APIException
):

    status_code = status.HTTP_400_BAD_REQUEST

    default_detail = 'An unknown ERROR occured'

    default_code = 'unknown_error'

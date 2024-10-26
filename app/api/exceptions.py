from rest_framework.exceptions import APIException
from rest_framework import status


class UnknownTicketType(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Unable to determin the ticket type.'
    default_code = 'unknown_ticket_type'

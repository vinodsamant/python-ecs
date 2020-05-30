"""
file to define custom exception for the projects
"""
# third-party
from rest_framework import status
from rest_framework.exceptions import APIException


class ValidationError(APIException):
    """
    custom validation error for the project to provide dict
    fields as defined
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        """initialize status_code if passed with exception
        otherwise pass default"""
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code

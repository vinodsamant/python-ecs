"""
file holds utility methods to be used in the project
"""
# standard library imports
import uuid
from decimal import Decimal
from functools import wraps

# django imports
from django.http import JsonResponse
from django.utils.decorators import available_attrs
# third-party
from rest_framework import status
from rest_framework.response import Response

# local Django
from base.exceptions import ValidationError
from base.messages import ERROR_CODE, INVALID_FIELD, REQUIRED


def required_post_params(params):
    """
    check required post param are in request or not
    :param params: request data params
    :return: function or error-message
    """

    def decorator(func):
        """
        decorator function to check required post param is present
        in request or not
        """

        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            """inner func to check required post param are in request or not"""
            if not all(param in request.data for param in params):
                return JsonResponse(
                    {
                        "detail": REQUIRED['MISSING_POST_PARAM'],
                        "status": False
                    },
                    status=status.HTTP_400_BAD_REQUEST)
            return func(request, *args, **kwargs)

        return inner

    return decorator


def required_get_params(params):
    """
    check required get param are in request or not
    :param params: query params
    :return: function or error-message
    """

    def decorator(func):
        """decorator func check required get param are in request or not"""

        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            """inner func check required get param are in request or not"""
            if not all(param in request.query_params for param in params):
                return JsonResponse(
                    {"detail": REQUIRED['MISSING_GET_PARAM'], "status": False},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return func(request, *args, **kwargs)

        return inner

    return decorator


def is_int(number):
    """
    validate number is integer or not.
    :param number: integer number
    :return: True/False
    """
    if number:
        try:
            int(number)
            return True
        except ValueError:
            pass
    return False


def success_response(data, response_code=None):
    """
    :param data: object passed in response
    :param response_code : response code for request default is 200
    :return: formatted success response in following format
             {
                'data': data,
                'status_code': response_code
            }
    """
    code = response_code if response_code else status.HTTP_200_OK
    return Response(
        {
            'data': data,
            'status_code': code
        },
        status=code
    )


def success_message_response(data):
    """
    return formatted success response for message string
    :param data:
    :return:following format response
        {
            'data': {'detail': data},
            'status_code': status.HTTP_200_OK
        }
    """
    return Response(
        {
            'data': {'detail': data},
            'status_code': status.HTTP_200_OK
        },
        status=status.HTTP_200_OK
    )


def validation_error(description):
    """
    Raise validation error in formatted dictionary
    """
    return ValidationError(
        {
            'detail': description,
            'status_code': int(status.HTTP_400_BAD_REQUEST)
        }
    )


def error_404(description):
    """ function to return error with status code"""
    raise ValidationError(
        detail={
            'detail': description,
            'status_code': status.HTTP_404_NOT_FOUND
        },
        status_code=status.HTTP_404_NOT_FOUND
    )


def get_object_or_404(model, *args, **kwargs):
    """
    return record with(args=kwargs) if available in model
    else return validation error
    :param model:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        raise error_404(
            description=ERROR_CODE['4004']
        )


NOT_FOUND = REQUIRED['NOT_FOUND'].format

MISSING_FIELD = REQUIRED['MISSING_KEY'].format

INVALID_FIELD = INVALID_FIELD.format


def for_all_methods(decorator):
    """Class decorator function which will apply to all the class method """

    def decorate(cls):
        """ decorator wrapper"""
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def get_random_string(string_length):
    """
    This method is to get random string.
    """
    return uuid.uuid4().hex[:string_length].upper()


def to_decimal(value):
    """
    :return: two decimal places decimal value
    """
    return Decimal("{0:.2f}".format(value))

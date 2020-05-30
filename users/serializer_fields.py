"""
custom fields for serializer defined here
"""
from rest_framework import serializers


class PasswordField(serializers.CharField):
    """
    custom serializer password field
    """

    def __init__(self, *args, **kwargs):
        """
        override constructor to make password as input type for this field
        """
        if 'style' not in kwargs:
            kwargs['style'] = {'input_type': 'password'}
        else:
            kwargs['style']['input_type'] = 'password'
        super(PasswordField, self).__init__(*args, **kwargs)

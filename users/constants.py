# Constant value of PASSWORD_LENGTH
from django.core.validators import RegexValidator

# Constant value of PASSWORD_LENGTH
PASSWORD_LENGTH = 8

# Constant value of PHONE_REGEX
PHONE_REGEX = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}$',
                             message="Phone number must not consist of space "
                                     "and requires country code. "
                                     "eg : +6591258565")
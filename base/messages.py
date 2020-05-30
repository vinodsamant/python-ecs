ERROR_CODE = {
    "4001": "Password should not be less than 8 characters.",
    "4002": "The password must be alphanumeric.",
    '4003': "Password and Confirm password didn't match.",
    '4004': "FB Access Token can not be blank.",
    '4005': "Twitter Access Token can not be blank.",
    '4006': "FB id can not be blank.",
    '4007': "User is not found.",
    '4008': "Username and Password didn't match.",
    '4009': "Current password is invalid.",
    '4010': "Input is invalid.",
}

MESSAGES = {
    "1001": "User is registered successfully.",
    "1002": "User is logout successfully.",
    "1003": "User profile is updated successfully.",
    "1004": "User password is verified successfully.",
}

# Message for REQUIRED fields which constants
# MISSING_POST_PARAM
# MISSING_GET_PARAM
# MISSING_KEY
# MISSING_FIELDS
# NOT_FOUND
REQUIRED = dict(
    MISSING_POST_PARAM='Required POST parameters not found.',
    MISSING_GET_PARAM='Required GET parameters not found.',
    MISSING_KEY="'{}' field is mandatory.",
    MISSING_FIELDS='Missing fields.',
    NOT_FOUND="'{}' not found."
)

# placeholder message for invalid field name
INVALID_FIELD = '\'{}\' field is not valid.'

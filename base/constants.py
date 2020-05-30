"""
Holds global constants related to project
"""
# response constants
STATUS_OK = 200
# Constant for STATUS_ERROR
STATUS_ERROR = 400
# Constant for CONST_OK
CONST_OK = 'OK'
# Constant for CONST_FAIL
CONST_FAIL = 'FAIL'

# Constant for DATE_TIME_FORMAT
DATE_TIME_FORMAT = '%m/%d/%Y %H:%M:%S'
# Constant for DATE_FORMAT
DATE_FORMAT = '%m/%d/%Y'
# Constant for DB_SORT_UPDATED_TIME
DB_SORT_UPDATED_TIME = '-updated_at'
# Constant for DB_SORT_CREATED_TIME
DB_SORT_CREATED_TIME = '-created_at'

# US specific local timezone
LOCAL_TIMEZONE = 'America/New_York'

# country code for number
COUNTRY_CODE = '+1'


class TableName:
    """ class to hold all table names """
    USERS = "users"
    OTP = "otp"
    SOCIAL_INFO = "social_info"

    STRIPE_ID = 'stripe_id'
    CREDIT_CARD = 'credit_card'
    BANK_ACCOUNT = 'bank_accounts'
    PAYOUTS = 'payouts'
    CONTEST_CATEGORY = 'contest_category'
    CONTESTS = 'contests'
    CONTEST_SUB_CATEGORY = 'contest_sub_category'


class URLPath:
    """class to hold url path segments"""
    # user
    CREATE_PASSWORD = 'create-password'
    UPDATE_PASSWORD = 'update-password'
    FORGOT_PASSWORD = 'forgot-password'
    RESET_FORGOT_PASSWORD = 'reset-forgot-password'
    VERIFY_PASSWORD = 'verify-password'
    VERIFY_NUMBER = 'verify-number'
    UPDATE_NUMBER = 'update-number'
    VERIFY_SOCIAL_NUMBER = 'verify-social-number'
    VERIFY_OTP = 'verify-otp'
    USER_DETAIL = 'detail'
    CONTACT_ADMIN_DETAIL = 'contact-admin'
    UPDATE_PROFILE = 'update-profile'
    UPDATE = 'update'
    LOGIN_WITH_PASSWORD = 'login-with-password'
    SOCIAL_LOGIN = 'social-login'
    LOGOUT = 'logout'

    # payments
    BANK_DETAIL = 'bank-detail'
    ADD_BANK_ACCOUNT = 'add-bank-account'
    KYC = 'kyc'
    ABOUT_KYC = 'about-kyc'
    SAVED_CARDS = 'saved-cards'
    ADD_CARD = 'add-card'
    DELETE_CARD = 'delete-card'
    CHARGE_CARD = 'charge-card'
    CHARGE_TOKEN = 'charge-token'
    STRIPE_EVENTS = 'stripe-events'


class RequestMethod:
    """class to hold request methods"""
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'
    PUT = 'put'
    DELETE = 'delete'


class SerializerFields:
    ALL = '__all__'
    USER_REGISTRATION_FIELDS = ('first_name', 'last_name', 'username',
                                'email', 'password', 'confirm_password', 'role')
    USER_SOCIAL_POST = ('fb_id', 'twitter_id', 'fb_access_token',
                        'twitter_access_token', 'twitter_access_token_secret')

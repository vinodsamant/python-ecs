"""
file to perform all timezone related operations
"""
import datetime as dt
from datetime import datetime

import pytz
from django.conf import settings
from django.utils import timezone

from base.constants import LOCAL_TIMEZONE


def get_current_datetime_in_local_tz():
    """ get current datetime in local timezone """
    return pytz.timezone(
        settings.TIME_ZONE
    ).localize(datetime.now()).astimezone(pytz.timezone(LOCAL_TIMEZONE))


def get_current_time():
    """
    :return: a timezone aware object in  UTC
    """
    return timezone.now()


def datetime_from_now(**kwargs):
    """
    :return: datetime with addition of kwargs timedelta
    """
    return timezone.now() + dt.timedelta(**kwargs)


def datetime_before_now(**kwargs):
    """
    :return: datetime with subtraction of kwargs timedelta
    """
    return timezone.now() - dt.timedelta(**kwargs)


def datetime_after_year():
    """
    :return: datetime after one year frm now
    """
    current_time = get_current_time()
    eod = dt.datetime(
        year=current_time.year,
        month=current_time.month,
        day=current_time.day
    ) + dt.timedelta(days=1, microseconds=-1)
    return pytz.timezone(
        LOCAL_TIMEZONE
    ).localize(eod.replace(year=current_time.year + 1))

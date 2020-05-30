"""
file to hold utility method for generating oauth token
"""
import os

from decouple import config
from django.db import transaction
from oauth2_provider.models import RefreshToken, Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token

from base.datetime_utils import datetime_from_now


def get_access_token(user):
    """
    removes old token attached with user
    create new token and access token for the user
    :param user: account instance
    :return: access-token in json format
    """
    app = Application.objects.get(client_secret=config('OAUTH_CLIENT_SECRET'),
                                  client_id=config('OAUTH_CLIENT_ID'))
    with transaction.atomic():
        if AccessToken.objects.filter(user=user).exists():
            clear_user(user)
        access_token_instance = AccessToken.objects.create(
            user=user, application=app,
            expires=datetime_from_now(
                seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            token=generate_token(),
            scope='read write'
        )
        RefreshToken.objects.create(
            user=user,
            application=app,
            token=generate_token(),
            access_token=access_token_instance
        )
        return access_token_instance.token


def get_token_json(instance):
    """
    :param instance: access token instance
    :return: json format of access-token, refresh-token with scope and expire time
    """
    token = {
        'access_token': instance.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'refresh_token': instance.refresh_token.token,
        'scope': instance.scope
    }

    return token


def clear_user(user):
    """removes user access token and his refresh token"""
    RefreshToken.objects.get(
        access_token=(AccessToken.objects.get(user=user))
    ).delete()
    AccessToken.objects.get(user=user).delete()

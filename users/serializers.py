import distutils
import re

from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import serializers

from base.choices import PROVIDER, ROLE_FB, ROLE_TWITTER
from base.constants import SerializerFields
from base.messages import ERROR_CODE
from base.utils import validation_error, success_response
from notifications.serializers import RegisterDeviceId
from users import choices
from users.constants import PASSWORD_LENGTH
from users.models import User, UserProfile
from users.oauth_util import get_access_token, clear_user
from users.serializer_fields import PasswordField


class RegistrationSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    first_name = serializers.CharField(required=True, max_length=128)
    last_name = serializers.CharField(required=True, max_length=128)
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)
    confirm_password = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)
    role = serializers.ChoiceField(choices=choices.ROLE, required=True)

    class Meta:
        model = User
        fields = SerializerFields.USER_REGISTRATION_FIELDS

    @staticmethod
    def get_confirm_password(obj):
        return obj

    def validate_password(self, password):
        """
        validating password
        :param password: string
        :return: boolean value based on success or failure of validation .
        """
        find_numeric = re.findall(r'\d', password)
        find_lowercase = re.findall('[a-z]', password)
        find_uppercase = re.findall('[A-Z]', password)
        count = 0
        if find_numeric:
            count = count + 1
        if find_lowercase:
            count = count + 1
        if find_uppercase:
            count = count + 1
        if count < 3:
            raise validation_error(ERROR_CODE["4002"])
        if not len(password) >= PASSWORD_LENGTH:
            raise validation_error(ERROR_CODE["4001"])

        return password

    def validate(self, attrs):
        """ validate if both the password match"""
        if attrs.get('password') != attrs.get('confirm_password'):
            raise validation_error(ERROR_CODE["4003"])
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data.get('password'))
        return user


class UserSocialPostSerializer(serializers.ModelSerializer):
    fb_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    twitter_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fb_access_token = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    twitter_access_token = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    twitter_access_token_secret = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = SerializerFields.USER_SOCIAL_POST


class LoginSerializer(RegisterDeviceId):
    username = serializers.CharField()

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(LoginSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        """ return username field"""
        try:
            username_field = get_user_model().USERNAME_FIELD
        except (ValueError, LookupError):
            username_field = 'username'

        return username_field

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        user_obj = User.objects.filter(Q(email=username) | Q(username=username)).first()
        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }

            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    super().update_device_id(self.initial_data, user)
                    return LoginResponseSerializer(user_obj).data
                raise validation_error(ERROR_CODE['4008'])
            raise validation_error(ERROR_CODE['4008'])
        raise validation_error(ERROR_CODE['4007'])


class LoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'token']

    @staticmethod
    def get_token(obj):
        return get_access_token(user=obj)


class LogoutSerializer(RegisterDeviceId):
    """
        This class is used to Logout user from the App.
    """

    def create(self, validated_data):
        """
        This method is used to logout on the basis of registration id.
        :param validated_data:
        :return:
        """
        user = self.context['request'].user
        user.logout()
        clear_user(user)
        return self


class UserProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    followers = serializers.CharField(read_only=True)
    following = serializers.CharField(read_only=True)
    fb_link = serializers.CharField(read_only=True)
    twitter_link = serializers.CharField(read_only=True)
    entered = serializers.CharField(read_only=True)
    won = serializers.CharField(read_only=True)
    votes = serializers.CharField(read_only=True)
    total_winnings = serializers.CharField(read_only=True)
    popularity = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['bio', 'image', 'followers', 'following',
                  'fb_link', 'twitter_link', 'entered',
                  'won', 'votes', 'total_winnings', 'popularity']


class UpdateUserProfileSerializer(UserProfileSerializer):
    name = serializers.CharField(required=True, max_length=128)
    username = serializers.CharField(required=True, max_length=150)
    # details = UserProfileSerializer()

    class Meta:
        model = User
        fields = UserProfileSerializer.Meta.fields + ['name', 'username']

    @staticmethod
    def get_details(obj):
        return UserProfile.objects.filter(user=obj)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        bio = validated_data.pop('bio')
        image = validated_data.pop('image')
        super(UpdateUserProfileSerializer, self).update(instance, validated_data)
        profile_obj = UserProfile.objects.filter(user=user)
        if profile_obj:
            profile_obj.update(bio=bio, image=image)
        else:
            UserProfile.objects.create(user=user, bio=bio, image=image)
        return instance


class VerifyUserByPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=100)

    class Meta:
        model = User
        fields = ['password', ]

    def validate_password(self, current_password):
        """
            check if password is true
        """
        user = self.context['request']
        if not user.check_password(current_password):
            raise validation_error(ERROR_CODE["4009"])
        return current_password


class SocialMediaSyncSerializer(serializers.ModelSerializer):
    is_synced = serializers.SerializerMethodField()
    provider = serializers.ChoiceField(required=True, choices=PROVIDER)

    class Meta:
        model = User
        fields = ['provider', 'is_synced']

    @staticmethod
    def get_is_synced(obj):
        return obj

    @staticmethod
    def strtobool(val):
        """Convert a string representation of truth to true (1) or false (0).

        True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
        are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
        'val' is anything else.
        """
        if type(val) == bool:
            return val, True
        if type(val) != str:
            return False, False
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return True, True
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return False, True
        else:
            return False, False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        provider = validated_data.get('provider', None)
        is_synced = validated_data.get('is_synced', None)
        is_synced, is_converted = self.strtobool(is_synced)
        if is_converted:
            obj_user = User.objects.get(id=user.id)
            if provider == ROLE_FB:
                obj_user.fb_sync = is_synced
            elif provider == ROLE_TWITTER:
                obj_user.twitter_sync = is_synced
            obj_user.save()
        else:
            raise validation_error(ERROR_CODE['4010'])
        return instance

from django.contrib.auth.models import AbstractUser
from django.db import models
from fcm_django.models import FCMDevice

from base.constants import TableName
from base.models import DateModel
from users.choices import ROLE
from users.managers import VierUserManager


class User(AbstractUser, DateModel):
    """
    Model to save users-authentication details
    """
    name = models.CharField(max_length=128, null=True)
    role = models.IntegerField(choices=ROLE)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    social_id = models.CharField(max_length=255, null=True)
    fb_id = models.TextField(null=True, blank=True)
    twitter_id = models.TextField(null=True, blank=True)
    provider = models.CharField(max_length=13, null=True)
    fb_access_token = models.TextField(null=True, blank=True)
    twitter_access_token = models.TextField(null=True, blank=True)
    twitter_access_token_secret = models.TextField(null=True, blank=True)
    fb_sync = models.BooleanField(default=False)
    twitter_sync = models.BooleanField(default=False)
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name='related_users',
                                   null=True, blank=True)
    verified = models.BooleanField(
        default=False, help_text="User password is created."
    )
    verified_email = models.BooleanField(
        default=False, help_text="User verified email."
    )
    profile_completed = models.BooleanField(
        default=False, help_text="User setup profile."
    )
    profile_picture = models.URLField(max_length=500, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    objects = VierUserManager()

    class Meta:
        """ meta class to provide user table name"""
        db_table = TableName.USERS

    def __str__(self):
        """ overriding default text for queryset for user class """
        return "{}_{}".format(self.username, self.role)

    def register_fcm_token(self, registration_id, device_type):
        """
        used to register dcm token
        """
        device, _ = FCMDevice.objects.get_or_create(user=self)
        device.registration_id = registration_id
        device.type = device_type
        device.active = True
        device.save()
        return device

    def send_push(self, data):
        """
        used to send push notification to the users
        :param data: data that we need to send
        :return: None
        """
        self.fcmdevice_set.filter(active=True).send_message(**data)

    def logout(self):
        """
        used to logout the user
        """
        FCMDevice.objects.filter(user=self).update(active=False)


def user_pic_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user/user_name__id/filename
    return 'user/{0}_{1}/{2}'.format(instance.user.name, instance.user.id, filename)


class UserProfile(DateModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_user')
    image = models.ImageField(null=True, blank=True, upload_to=user_pic_path)
    followers = models.IntegerField(default=0, null=True, blank=True)
    following = models.IntegerField(default=0, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    fb_link = models.TextField(blank=True, null=True)
    twitter_link = models.TextField(blank=True, null=True)
    entered = models.IntegerField(default=0, null=True, blank=True)
    won = models.IntegerField(default=0, null=True, blank=True)
    votes = models.IntegerField(default=0, null=True, blank=True)
    total_winnings = models.IntegerField(default=0, null=True, blank=True)
    popularity = models.IntegerField(default=0, null=True, blank=True)

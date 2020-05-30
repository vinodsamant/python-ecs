"""
Custom user manager
"""
from django.contrib.auth.models import UserManager
from django.db import transaction


class VierUserManager(UserManager):
    """  Custom user VierUserManager """

    def _create_user(self, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        with transaction.atomic():
            username = extra_fields.pop('username')
            user = self.model(**extra_fields)
            user.username = username
            user.set_password(extra_fields.get('password', None))
            user.save(using=self._db)
            return user

    def create_user(self, **extra_fields):
        """ normal user creation """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(**extra_fields)

    def create_superuser(self, *args, **kwargs):
        """
        initialises 'is_staff' and 'is_superuser' to 'True' for superuser
        :param args: login credentials
        :param kwargs: login credentials
        :return: user instance
        """
        # To prevent unique constraint failed for email after saving user
        user = self.create_user(*args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.verified = True
        user.profile_completed = True
        user.save(using=self._db)
        return user

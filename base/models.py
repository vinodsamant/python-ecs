from django.db import models


class DateModel(models.Model):
    """
        Base date model for other models holding created and updated
        datetime of record
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ table information to make it abstract """
        abstract = True

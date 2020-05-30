from django.db import models

from base.models import DateModel
from base.choices import PROVIDER
from users.models import User


def fb_pic_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/contest__id/user_name__id/filename
    return 'contest_{0}/{1}_{2}/{3}'.format(instance.id,
                                            instance.user.name,
                                            instance.user.id,
                                            filename)


class UserContestsModel(DateModel):
    user = models.ForeignKey(User, models.CASCADE)
    # contest = models.ForeignKey(ContestsModel, models.CASCADE)
    fb_feed_id = models.CharField(max_length=150, null=True, blank=True)
    twitter_feed_id = models.CharField(max_length=150, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    fb_image = models.ImageField(null=True, blank=True, upload_to=fb_pic_path)
    content = models.TextField(null=True, blank=True)
    fb_likes_count = models.CharField(max_length=150, null=True, blank=True)
    twitter_likes_count = models.CharField(max_length=150, null=True, blank=True)
    comments_count = models.CharField(max_length=150, null=True, blank=True)
    provider = models.IntegerField(choices=PROVIDER)
    rank = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    address = models.TextField()

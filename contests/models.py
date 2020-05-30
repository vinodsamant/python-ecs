from django.db import models

from base.choices import PRIZE_RANGE_TYPE, PRIZE_TYPE
from base.constants import TableName
from base.media_upload_s3 import file_name_creater
from base.models import DateModel
from contest_categories.models import ContestSubCategory
from users.models import User


def logo_directory(instance, filename):
    """ AWS directory path to store job image """
    # file will be uploaded to MEDIA_ROOT/job/User_name__id/filename
    return 'contest/logo/{0}_{1}/{2}'.format(
        instance.user.username,
        instance.contest_name,
        str(file_name_creater()) + "." + str(filename.split(".")[-1]))


def gift_card_directory(instance, filename):
    """ AWS directory path to store job image """
    # file will be uploaded to MEDIA_ROOT/job/User_name__id/filename
    return 'contest/gift_card/{0}_{1}/{2}'.format(
        instance.user.username,
        instance.contest_name,
        str(file_name_creater()) + "." + str(filename.split(".")[-1]))


def ad_video_directory(instance, filename):
    """ AWS directory path to store job image """
    # file will be uploaded to MEDIA_ROOT/job/User_name__id/filename
    return 'contest/ad_video/{0}_{1}/{2}'.format(
        instance.user.username,
        instance.contest_name,
        str(file_name_creater()) + "." + str(filename.split(".")[-1]))


class ContestsModel(DateModel):
    """
    This model is used to save data of contest.
    """
    user = models.ForeignKey(User, models.CASCADE)
    contest_name = models.CharField(max_length=150, null=True, blank=True)
    contest_internal_name = models.CharField(max_length=150, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)
    brand_name = models.CharField(max_length=150, null=True, blank=True)
    prize_money = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(null=True, upload_to=logo_directory)
    gift_card = models.FileField(blank=True, null=True, verbose_name='Upload gift card',
                                 upload_to=gift_card_directory)
    qualification_eligibility = models.IntegerField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    terms_and_conditions = models.TextField(null=True, blank=True)
    ad_video = models.FileField(blank=True, null=True, verbose_name='Upload ad video',
                                upload_to=ad_video_directory)
    cpm_daily_max_spend = models.IntegerField(null=True, blank=True)
    cpc_ad_description = models.TextField(null=True, blank=True)
    ad_url = models.TextField(null=True, blank=True)
    cpc_daily_max_spend = models.IntegerField(null=True, blank=True)

    class Meta:
        """
        This is used to provide table name.
        """
        db_table = TableName.CONTESTS

    def __str__(self):
        """
        This is used to set the text of string. Which is return from queryset.
        :return:
        """
        return "{}__{}".format(self.contest_name, self.user)


class ContestCategory(DateModel):
    """
        This class is used to set the category of any contest.
    """

    contest = models.ForeignKey(ContestsModel, on_delete=models.CASCADE)
    category = models.ForeignKey(ContestSubCategory, on_delete=models.CASCADE)


class ContestPrize(DateModel):
    """
    This model is used to set multiple prize for contest.
    """
    contest = models.ForeignKey(ContestsModel, on_delete=models.CASCADE)
    prize_range_type = models.IntegerField(choices=PRIZE_RANGE_TYPE)
    rank = models.IntegerField(default=0, null=True, blank=True)
    from_range = models.IntegerField(default=0, null=True, blank=True)
    to_range = models.IntegerField(default=0, null=True, blank=True)
    prize_type = models.IntegerField(choices=PRIZE_TYPE)

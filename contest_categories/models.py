from django.db import models

# Create your models here.
from base.constants import TableName
from base.models import DateModel


class ContestCategory(DateModel):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = TableName.CONTEST_CATEGORY


class ContestSubCategory(DateModel):
    category = models.ForeignKey(ContestCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    cpc_price = models.PositiveIntegerField(max_length=20)
    cpm_price = models.PositiveIntegerField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = TableName.CONTEST_SUB_CATEGORY



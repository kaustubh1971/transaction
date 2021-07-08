import random
from datetime import date

from django.db import models
from django.db.models.base import Model
from django_extensions.db.fields import CreationDateTimeField,\
    ModificationDateTimeField

class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "CompanyLedgerMaster"
        verbose_name_plural = "CompanyLedgerMasters"

    def __str__(self):
        return self.name


class BranchMaster(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "BranchMaster"
        verbose_name_plural = "BranchMasters"

    def __str__(self):
        return self.name



class DepartmentMaster(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "DepartmentMaster"
        verbose_name_plural = "DepartmentMasters"

    def __str__(self):
        return self.name


class ArticleMaster(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "ArticleMaster"
        verbose_name_plural = "ArticleMaster"

    def __str__(self):
        return self.name


class ColorMaster(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "ColorMaster"
        verbose_name_plural = "ColorMaster"

    def __str__(self):
        return self.name


class Inventory(models.Model):
    status_choices = (('KG', 'KG'),
					 ('METER', 'METER'))
    company = models.ForeignKey(CompanyLedgerMaster,
        null=True, on_delete=models.DO_NOTHING)
    article =  models.ForeignKey(ArticleMaster,
        null=True, on_delete=models.CASCADE)
    color =  models.ForeignKey(ColorMaster,
        null=True, on_delete=models.CASCADE)
    gross_quantity = models.FloatField(null=True)
    net_quantity = models.FloatField(null=True)
    unit = models.CharField(max_length=50, null=True, 
        choices=status_choices)
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


class TransactionLine(models.Model):
    status_choices = (('KG', 'KG'),
					 ('METER', 'METER'))

    inventory = models.ManyToManyField(Inventory,
        related_name='inventory_line',
        blank= True
        )
    article =  models.ForeignKey(ArticleMaster,
        null=True, on_delete=models.CASCADE)
    color =  models.ForeignKey(ColorMaster,
        null=True, on_delete=models.CASCADE)
    required_on_date = models.DateField(null=True,blank=True)
    quantity = models.FloatField(null=True)
    rate_per_unit = models.IntegerField(null=True)
    unit = models.CharField(max_length=50, null=True, 
        choices=status_choices)
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


def generate_transaction_id():
    transaction_id = "" + "".join(
        [random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVXYZ') for i in range(8)]
        )
    tran_id = "TRN"+transaction_id + '1' + str(date.today().year)
    return tran_id

class Transaction(models.Model):
    status_choices = (('PENDING', 'PENDING'),
					 ('COMPLETED', 'COMPLETED'),
					 ('CLOSE', 'CLOSE'))
    company = models.ForeignKey(CompanyLedgerMaster,
        null=True, on_delete=models.DO_NOTHING)
    branch = models.ForeignKey(BranchMaster,
        null=True, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(DepartmentMaster,
        null=True, on_delete=models.DO_NOTHING)
    tran_line = models.ManyToManyField(TransactionLine,
        related_name='transaction_time_line',
        blank= True
        )
    tran_number = models.CharField(max_length=100, 
        editable=False, default=generate_transaction_id, 
        unique=True, db_index = True)
    status = models.CharField(max_length=50, null=True, 
        choices = status_choices)
    remark = models.TextField(null=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

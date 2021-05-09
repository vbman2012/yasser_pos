import uuid
from django.db import models
from django.db.models.enums import Choices
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from apps.accounts.models import MasterBranches, PhoneBook, BankMaster
from django.urls import reverse

''' الاصول = الاتزامات + رأس المال - المسحوبات الشخصية + الايرادات - المصروفات'''
class AccountType(models.Model):
    type_name = models.CharField(max_length=50, null=False, blank=False)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=0)


    def __str__(self):
        return f"{self.id} : {self.type_name}"


class AccountGroup(models.Model):
    acg_serial = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name="parents")
    acg_code = models.BigIntegerField(unique=True)
    acg_name = models.CharField(max_length=200)
    acg_level = models.IntegerField()
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE,
                             related_name="AccountGroups")
    tot_credit = models.DecimalField(max_digits=11, decimal_places=2)
    tot_debit = models.DecimalField(max_digits=11, decimal_places=2)
    balance = models.DecimalField(max_digits=11, decimal_places=2)


    def get_group_type(self):
        return self.type

    # get name show in admin
    def __str__(self):
        return f"{ self.acg_code }: { self.acg_name}"


class AccountMaster(models.Model):
    acc_serial = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    account_group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE,
                                      related_name="Accounts_master")
    acc_code = models.BigIntegerField(unique=True)
    acc_name = models.CharField(max_length=200)
    acc_level = models.IntegerField()
    is_active = models.BooleanField(default=True)
    opening_credit = models.DecimalField(max_digits=11, decimal_places=2)
    opening_debit = models.DecimalField(max_digits=11, decimal_places=2)
    credit = models.DecimalField(max_digits=11, decimal_places=2)
    debit = models.DecimalField(max_digits=11, decimal_places=2)
    balance = models.DecimalField(max_digits=11, decimal_places=2)
    can_edit = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('account-detail', kwargs={'pk': self.acc_serial})

    def get_account_group(self):
        return self.account_group

    def __str__(self):
        return f"{ self.acc_code }: { self.acc_name}"


class AccountBalance(models.Model):
    account_master = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                       related_name='Accounts_balance')
    opening_Balance_dr = models.DecimalField(max_digits=9, decimal_places=2)
    opening_Balance_cr = models.DecimalField(max_digits=9, decimal_places=2)
    tran_total_credit = models.DecimalField(max_digits=11, decimal_places=2)
    tran_total_debit = models.DecimalField(max_digits=11, decimal_places=2)
    current_balance = models.DecimalField(max_digits=9, decimal_places=2)
    update_balance = models.DecimalField(max_digits=9, decimal_places=2)
    master_branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE,
                                      related_name='Accounts_balance')

    def get_account_balance(self):
        return self.account_master

    def __str__(self):
        return (f"{ self.account_master } - { self.current_balance } -"
                f"'branch is :' { self.master_branch }")

class CustomerMaster(models.Model):
    account_master = models.ForeignKey(AccountMaster, on_delete=models.CASCADE)
    phone_book = models.ForeignKey(PhoneBook, on_delete=models.CASCADE,
                                   related_name='customers')
    start_date = models.DateTimeField(auto_now_add=True, blank=False)
    credit_limit = models.DecimalField(max_digits=9, decimal_places=2)
    contact_name = models.CharField(max_length=150, blank=True)
    contact_title = models.CharField(max_length=150, blank=True)


class CustomerDue(models.Model):
    customer_account = models.ForeignKey(CustomerMaster,
                                         on_delete=models.CASCADE,
                                         related_name='customers_due')
    total_debit = models.DecimalField(max_digits=9, decimal_places=2)
    total_credit = models.DecimalField(max_digits=9, decimal_places=2)
    overdays_count = models.IntegerField()
    cust_due_branch = models.ForeignKey(MasterBranches,
                                        on_delete=models.CASCADE,
                                        related_name='customers_due')


class SupplierMaster(models.Model):
    supplier_account = models.ForeignKey(AccountMaster,
                                         on_delete=models.CASCADE,
                                         related_name='suppliers')
    phone_book = models.ForeignKey(PhoneBook, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True, blank=False)
    credit_limit = models.DecimalField(max_digits=9, decimal_places=2)
    contact_name = models.CharField(max_length=150, blank=True)
    contact_title = models.CharField(max_length=150, blank=True)
    bank_master = models.ForeignKey(BankMaster, on_delete=models.CASCADE)
    Bank_Account_no = models.CharField(max_length=50)

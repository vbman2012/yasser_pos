import uuid
from django.db import models
from django.db.models.enums import Choices
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from apps.accounts.models import (MasterBranches, PhoneBook, BankMaster,
                                  ModeOfPay_CHOICES)
from apps.accounting.models import AccountMaster
from apps.product.models import Product
from django.urls import reverse



class IncomesVoucher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt_no = models.BigIntegerField()
    receipt_date = models.DateTimeField()
    customer = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                 related_name='customer_incomes')
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    cash = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                        related_name='cash_incomes')
    br_description = models.CharField(max_length=500)
    init_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='incomes')


class ExpensesVoucher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt_no = models.BigIntegerField()
    receipt_date = models.DateTimeField()
    main_code = models.IntegerField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    cash = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                            related_name='cash_expenses')
    supplier = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                        related_name='supplier_expenses')
    cp_description = models.CharField(max_length=500)
    init_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='expenses')


class SalesInvoiceMaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.BigIntegerField()
    invoice_date = models.DateTimeField()
    customer = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                 related_name='sales_invoices')
    grand_amount = models.DecimalField(max_digits=9, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2)
    mode_of_pay = models.CharField(max_length=3, choices=ModeOfPay_CHOICES,
                                   default='CAS')
    description = models.CharField(max_length=500)
    init_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='sales_invoices')


class SalesInvoiceDetail(models.Model):
    sales_invoice = models.ForeignKey(SalesInvoiceMaster,
                                      on_delete=models.CASCADE,
                                      related_name='sales_invoice_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='sales_invoice_details')
    qnty = models.IntegerField(default=1)
    sales_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0)
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                          default=0)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0)


class PurchaseInvoiceMaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.BigIntegerField()
    invoice_date = models.DateTimeField()
    supplier = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                 related_name='purchase_invoices')
    grand_amount = models.DecimalField(max_digits=9, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2)
    mode_of_pay = models.CharField(max_length=3, choices=ModeOfPay_CHOICES,
                                   default='CAS')
    description = models.CharField(max_length=500)
    init_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='purchase_invoices')


class PurchaseInvoiceDetail(models.Model):
    pruchase_invoice = models.ForeignKey(PurchaseInvoiceMaster,
                                      on_delete=models.CASCADE,
                                      related_name='purchaes_invoice_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='purchase_invoice_details')
    qnty = models.IntegerField(default=1)
    cost_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0)
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                          default=0)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0)


class SalesReturnMaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_no = models.BigIntegerField()
    invoice_date = models.DateTimeField()
    customer = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                 related_name='sales_returns')
    grand_amount = models.DecimalField(max_digits=9, decimal_places=2)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2)
    mode_of_pay = models.CharField(max_length=3, choices=ModeOfPay_CHOICES,
                                   default='CAS')
    description = models.CharField(max_length=500)
    init_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='sales_returns')


class SalesReturnDetail(models.Model):
    return_invoice = models.ForeignKey(SalesReturnMaster,
                                      on_delete=models.CASCADE,
                                      related_name='sales_return_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='sales_return_details')
    qnty = models.IntegerField(default=1)
    sales_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0)


class PurchaseReturnMaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_no = models.BigIntegerField()
    invoice_date = models.DateTimeField()
    supplier = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,
                                 related_name='purchase_returns')
    grand_amount = models.DecimalField(max_digits=9, decimal_places=2)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2)
    mode_of_pay = models.CharField(max_length=3, choices=ModeOfPay_CHOICES,
                                   default='CAS')
    description = models.CharField(max_length=500)
    init_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='purchase_returns')


class PurchaseReturnDetail(models.Model):
    return_invoice = models.ForeignKey(PurchaseReturnMaster,
                                      on_delete=models.CASCADE,
                                      related_name='purchase_return_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='purchase_return_details')
    qnty = models.IntegerField(default=1)
    cost_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0)

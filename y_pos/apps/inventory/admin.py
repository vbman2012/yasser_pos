from django.contrib import admin
from .models import (
    IncomesVoucher,
    ExpensesVoucher,
    SalesInvoiceMaster,
    SalesInvoiceDetail,
    PurchaseInvoiceMaster,
    PurchaseInvoiceDetail,
    SalesReturnMaster,
    SalesReturnDetail,
    PurchaseReturnMaster,
    PurchaseReturnDetail
)

admin.site.register(IncomesVoucher)
admin.site.register(ExpensesVoucher)
admin.site.register(SalesInvoiceMaster)
admin.site.register(SalesInvoiceDetail)
admin.site.register(PurchaseInvoiceMaster)
admin.site.register(PurchaseInvoiceDetail)
admin.site.register(SalesReturnMaster)
admin.site.register(SalesReturnDetail)
admin.site.register(PurchaseReturnMaster)
admin.site.register(PurchaseReturnDetail)

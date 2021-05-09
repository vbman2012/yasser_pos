from django.contrib import admin
from .models import (AccountType, AccountGroup, AccountMaster, AccountBalance,
                     CustomerMaster, CustomerDue, SupplierMaster)


admin.site.register(AccountType)
admin.site.register(AccountGroup)
admin.site.register(AccountMaster)
admin.site.register(AccountBalance)
admin.site.register(CustomerMaster)
admin.site.register(CustomerDue)
admin.site.register(SupplierMaster)

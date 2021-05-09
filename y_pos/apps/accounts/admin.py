from django.contrib import admin
from .models import (
    Profile,
    CountryMaster,
    CityMaster,
    MohafzaOfCity,
    PhoneBook,
    BankMaster,
    BankBranches,
    IDCardMaster,
    JobsMaster,
    CompanyMaster,
    MasterBranches
)


admin.site.register(Profile)
admin.site.register(CountryMaster)
admin.site.register(MohafzaOfCity)
admin.site.register(CityMaster)
admin.site.register(PhoneBook)
admin.site.register(BankMaster)
admin.site.register(BankBranches)
admin.site.register(IDCardMaster)
admin.site.register(JobsMaster)
admin.site.register(CompanyMaster)
admin.site.register(MasterBranches)

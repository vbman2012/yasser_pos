import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDER_CHOICES = [
    ('ME', 'ذكر'),
    ('FE', 'انثي'),
]

ModeOfPay_CHOICES = [
    ('CAS', 'كاش'),
    ('CRE', 'اجل'),
]


def user_directory(instance, filename):
    return 'users/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=450, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )


class CountryMaster(models.Model):
    name_ar = models.CharField(max_length=35, blank=True)
    name_en = models.CharField(max_length=35, blank=True)
    region = models.CharField(max_length=35, blank=True)
    currency = models.CharField(max_length=5, blank=True)


class MohafzaOfCity(models.Model):
    country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, related_name='%(class)s_mohafzes_country')
    name_ar = models.CharField(max_length=35, blank=True)
    name_en = models.CharField(max_length=35, blank=True)


class CityMaster(models.Model):
    mohafza = models.ForeignKey(MohafzaOfCity, on_delete=models.CASCADE, related_name='%(class)s_cites_mohafza')
    name_ar = models.CharField(max_length=35, blank=True)
    name_en = models.CharField(max_length=35, blank=True)


class PhoneBook(models.Model):
    city = models.ForeignKey(CityMaster, on_delete=models.CASCADE, related_name='%(class)s_phons_city')
    address = models.CharField(max_length=250, blank=True)
    phone_no_1 = models.CharField(max_length=15, blank=True)
    phone_no_2 = models.CharField(max_length=15, blank=True)
    fax_no =   models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    mobile_no_1 = models.CharField(max_length=15, blank=True)
    mobile_no_2 = models.CharField(max_length=15, blank=True)
    work_phone_no = models.CharField(max_length=15, blank=True)


class BankMaster(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)


class BankBranches(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    bank_master = models.ForeignKey(BankMaster, on_delete=models.CASCADE, related_name='%(class)s_branches_bank')
    city = models.ForeignKey(CityMaster, on_delete=models.CASCADE, related_name='%(class)s_banks_city')


class IDCardMaster(models.Model):
    IDTYPE_CHOICES =[
        ('PI', 'PERSONAL CARD'),
        ('VI', 'VISA'),
        ('DR', 'DRIVER LICENSE'),
        ('WO', 'WORK LICENSE'),
        ('HI', 'Health Insurance'),
        ('BI', 'BANK CARD'),
    ]
    id_no = models.BigIntegerField()
    id_source = models.CharField(max_length=20)
    id_end_date = models.DateTimeField()
    responsible_no = models.BigIntegerField()
    responsible_name = models.CharField(max_length=150)
    id_type = models.CharField(max_length=2, choices=IDTYPE_CHOICES, default="PERSONAL CARD")
    phone_book = models.ForeignKey(PhoneBook, on_delete=models.CASCADE, related_name='%(class)s_cards_phone')
    image = models.ImageField(upload_to='images/', blank=True, null=True)

class JobsMaster(models.Model):
    job_title_ar = models.CharField(max_length=50)
    job_title_en = models.CharField(max_length=50)


class CompanyMaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    no = models.PositiveSmallIntegerField()
    name_ar = models.CharField(max_length=150, blank=False, null=False, unique=True)
    name_en = models.CharField(max_length=150, blank=False, null=False, unique=True)
    reg_no = models.CharField(max_length=50, blank=True)
    vat_no = models.CharField(max_length=50, blank=True)
    main_logo_ar = models.ImageField(upload_to='images/', blank=True, null=True)
    main_logo_en = models.ImageField(upload_to='images/', blank=True, null=True)
    website = models.URLField(max_length=100, blank=True)
    owner_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    phone_book = models.ForeignKey(PhoneBook, on_delete=models.CASCADE, related_name='%(class)s_companies_phone')

    def __str__(self):
        return f'{self.no} : {self.name_ar}'

    def save(self):
        num = 0
        if not CompanyMaster.objects.order_by('no').last():
            self.no = 1
        else:
            self.no = CompanyMaster.objects.order_by('no').last().no + 1
        super(CompanyMaster, self).save()


class MasterBranches(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(CompanyMaster, on_delete=models.CASCADE, related_name='%(class)s_branches_company')
    no = models.PositiveSmallIntegerField()
    name_ar = models.CharField(max_length=150, blank=False, null=False, unique=True)
    name_en = models.CharField(max_length=150, blank=False, null=False, unique=True)
    vat_percentag = models.DecimalField(max_digits=3, decimal_places=2)
    main_logo_ar = models.ImageField(upload_to='images/', blank=True, null=True)
    main_logo_en = models.ImageField(upload_to='images/', blank=True, null=True)
    website = models.URLField(max_length=100, blank=True)
    manager_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    allow_credit = models.BooleanField(default=False)
    bank_master = models.ForeignKey(BankMaster, on_delete=models.CASCADE, related_name='%(class)s_branches_bank')

    def __str__(self):
        return f'{self.company}--{self.no} : {self.name_ar}'

    def save(self):
        num = 0
        if not MasterBranches.objects.order_by('no').last():
            self.no = 1
        else:
            self.no = MasterBranches.objects.order_by('no').last().no + 1
        super(MasterBranches, self).save()

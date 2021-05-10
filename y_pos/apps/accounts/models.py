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


class PhoneBook(models.Model):
    city = models.CharField(max_length=250, default="المنصورة")
    address = models.CharField(max_length=250, default="عنوان")
    phone_no_1 = models.CharField(max_length=15, default="رقم هاتف 1")
    phone_no_2 = models.CharField(max_length=15, default="رقم هاتف 2")
    email = models.EmailField(max_length=50, default="yasser@pos.com")
    mobile_no_1 = models.CharField(max_length=15, default="موبايل 1")
    mobile_no_2 = models.CharField(max_length=15, default="موبايل 2")
    work_phone_no = models.CharField(max_length=15, default="هاتف عمل 2")
    notes = models.CharField(max_length=550, default="ملاحظات")


class BankMaster(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)



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

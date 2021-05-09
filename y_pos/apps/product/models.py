from django.db import models
from apps.accounts.models import MasterBranches

def product_directory(instance, filename):
    return 'products/product_{0}/{1}'.format(instance.product.id, filename)


class ProductCategory(models.Model):
    name = models.CharField(max_length=55)


class Product(models.Model):
    name = models.CharField(max_length=75)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 related_name="products")
    image = models.ImageField(max_length=1200, upload_to=product_directory)
    init_date = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=25)
    notes = models.CharField(max_length=255)


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_details')
    description = models.CharField(max_length=450, default="description")
    current_qnty = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0)
    sales_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0)
    status = models.BooleanField(default=True)
    expier_date = models.DateTimeField()
    branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='product_details')

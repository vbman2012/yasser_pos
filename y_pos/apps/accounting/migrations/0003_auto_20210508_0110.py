# Generated by Django 3.2 on 2021-05-08 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_delete_supplierdue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountmaster',
            old_name='acc_name_ar',
            new_name='acc_name',
        ),
        migrations.RemoveField(
            model_name='accountmaster',
            name='acc_name_en',
        ),
    ]

# Generated by Django 4.2.5 on 2023-11-25 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0004_rename_name_vendor_vendorserializer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='VendorSerializer',
            new_name='name',
        ),
    ]
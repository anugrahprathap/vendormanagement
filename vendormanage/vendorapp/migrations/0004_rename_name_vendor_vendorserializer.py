# Generated by Django 4.2.5 on 2023-11-25 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0003_alter_vendor_uid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='name',
            new_name='VendorSerializer',
        ),
    ]

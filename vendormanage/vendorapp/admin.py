from django.contrib import admin
from .models import PurchaseOrder, Vendor
# Register your models here.
admin.site.register(Vendor)
admin.site.register(PurchaseOrder )
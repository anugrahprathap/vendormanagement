
from rest_framework import serializers
from .models import Vendor, PurchaseOrder
from django.contrib.auth.models import User


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

# Serilizer fro creating a purchase order
class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()
    class Meta:
        model = PurchaseOrder
        fields = ['items','order_date','delivery_date','quantity','quality_rating','status','issue_date','acknowledgment_date']
    


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        # Select only the perfromance related details from vendor
        fields = ['name','vendor_code','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']
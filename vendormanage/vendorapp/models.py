# models.py

from django.utils import timezone
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

# Vendor Model
class Vendor(models.Model):
    uid =  models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(default=0,null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    # Function to calculate average response time
    def update_average_response_time(self, new_response_time):
    # If average_response_time is negative, set it to the new response time
        if self.average_response_time ==-1:
            self.average_response_time = new_response_time
        else:
            # Calculate the new average
            if(self.get_total_orders()>0):
                print('*'*89)
                print(self.average_response_time,self.get_total_orders())
                total_response_time =0
                if self.average_response_time:
                    total_response_time = self.average_response_time * self.get_total_orders()
                total_response_time += new_response_time
                self.average_response_time = total_response_time / (self.get_total_orders() + 1)

    # Function to calculate fulfillment rate
    def update_fulfillment_rate(self,status):
        
        total_orders = self.get_total_orders()
        if total_orders == 0:
            
            self.fulfillment_rate = None
        else:
            successfully_fulfilled_orders = self.purchaseorder_set.filter(status='completed',vendor=self).count()
            if(status=='completed' or status=='canceled'):
                if(status=='completed'):
                    successfully_fulfilled_orders +=1
                self.fulfillment_rate = (successfully_fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0
            else:
                self.fulfillment_rate = (successfully_fulfilled_orders /( total_orders)) * 100 if total_orders > 0 else 0
        self.save()

       

       
   
    from decimal import Decimal
    # Function to calcualte on time delevery rate
    def update_ontime_delivary_date(self, delivery_date):
        total_completed_orders = self.purchaseorder_set.filter(status='completed',vendor=self).count()

        if total_completed_orders == 0:
            self.on_time_delivery_rate = Decimal(100)  # Assume 100% on-time delivery for no completed orders
        
            self.on_time_delivery_rate = Decimal(100) if delivery_date >= timezone.now() else Decimal(0)
        elif total_completed_orders > 0:
            on_time_deliver_items = (total_completed_orders) * Decimal(str(self.on_time_delivery_rate)) / Decimal(100)


            if delivery_date >= timezone.now():
                on_time_deliver_items += Decimal(1)

            self.on_time_delivery_rate = (on_time_deliver_items / Decimal(total_completed_orders+1)) * Decimal(100)
            
        
        self.save()
        
    # To calculate average quality rating
    def update_quality_rating_avg(self):
        total_quality_ratings = self.purchaseorder_set.filter(status='completed').exclude(quality_rating__isnull=True).count()
        if total_quality_ratings > 0:
            sum_quality_ratings = self.purchaseorder_set.filter(status='completed').exclude(quality_rating__isnull=True).aggregate(models.Sum('quality_rating'))['quality_rating__sum']
            self.quality_rating_avg = sum_quality_ratings / total_quality_ratings
        else:
            self.quality_rating_avg = None
        self.save()


    # To calculate total orders
    def get_total_orders(self):
        return self.purchaseorder_set.filter(vendor=self).count()
    def __str__(self):
        return self.name
    



    



# Purchase order model
class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True,blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

   



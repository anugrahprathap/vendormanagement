# signals.py
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(pre_save, sender=PurchaseOrder) # Tells the signal that these change should occur before the instence is saved
@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_statistics(sender, instance, **kwargs):
    """
    Update vendor statistics (average_response_time, fulfillment_rate, on_time_delivery_rate)
    whenever a PurchaseOrder is about to be saved or deleted, but only if the status has changed.
    """
    if instance.pk:  # Check if the instance is not a new one (already saved)
        try:
            previous_instance = PurchaseOrder.objects.get(pk=instance.pk)  # Retrieve previous state
            if instance.status != previous_instance.status:
                vendor = instance.vendor
                 # Invoke update_average_response_time() if the vendor acknowledged or reject the order
                if instance.status == 'acknowledged' or instance.status == 'rejected':
                    response_time = (instance.acknowledgment_date - instance.order_date).total_seconds()
                    vendor.update_average_response_time(response_time)
                # Invoke update_ontime_delivary_date() if the status change to completed
                if instance.status == 'completed':
                    vendor.update_ontime_delivary_date(instance.delivery_date)
                vendor.update_fulfillment_rate(instance.status)
        except PurchaseOrder.DoesNotExist:
            pass  # Handle the case where the previous instance does not exist
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_quality_rating(sender, instance, created, **kwargs):
    """
    Update the average quality rating for the associated Vendor whenever a PurchaseOrder 
    is saved, but only if the quality_rating is not null in the purchase order instance.
    """
    if not created:
        try:
           
            if instance.quality_rating :
                vendor = instance.vendor
                vendor.update_quality_rating_avg()
        except PurchaseOrder.DoesNotExist:
            pass  # Handle the case where the previous instance does not exist (e.g., for a new instance)
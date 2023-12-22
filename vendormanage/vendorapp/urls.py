# vendor_management/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/login/', LoginView.as_view(), name='vendor-login'),
    path('api/vendors/purchase-orders/', PurchaseOrderListForVendor.as_view(), name='purchase-order-list-for-vendor'),

    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('api/purchase/',PurchaseOrderCreate.as_view(),name='purchase-order-create'),
    path('api/purchase-orders/', PurchaseOrderListForAdmin.as_view(), name='purchase-order-list-admin'),
    path('api/purchase-order/<int:pk>/',PurchaseOrderUpdateDeleteView.as_view(),name='purchase-order-retrieve-update-delete'),
    path('api/vendors/<int:pk>/performance/',VendorPerformenceView.as_view(),name='vendor-performance'),
]

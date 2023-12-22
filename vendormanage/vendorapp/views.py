
# views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User  # Assuming you're using the default User model
from .models import Vendor,PurchaseOrder
from .serializers import VendorPerformanceSerializer,VendorSerializer,PurchaseOrderSerializer,UserSerializer,PurchaseOrderCreateSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser

# Vendor Create and View 
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def perform_create(self, serializer):

        username = self.request.data.get('username')

        
        existing_user = User.objects.filter(username=username).first()
        print(existing_user)
        if  existing_user==None:
            
            password=self.request.data.get('password')
            hashed_password = make_password(password)
            user_data = {
                'username': self.request.data.get('username'), 
                'password': hashed_password,    
            }

        
            
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()

                # Associate the user with the vendor
                serializer.save(uid=user)
                return Response({'success': 'User and vendor created successfully'}, status=status.HTTP_201_CREATED)

            else:
                # If user data is invalid, return an error response
                return Response({'error': 'Invalid user data'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('*'*89)
            
            print('User Exits')
            return "errror"
        
        

        
        
        

# Login API

from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not (username and password):
            return Response({'error': 'Please provide both username and password for login.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            # Generate a refresh token
            refresh = RefreshToken.for_user(user)

            # Check if the user is a vendor
            is_vendor = Vendor.objects.filter(uid=user).exists()

            # Add the role information to the user
            user_role = 'vendor' if is_vendor else 'regular_user'

            # Send relevant data after successful login
            response_data = {
                
                'token': str(refresh.access_token),
                
                'role': user_role,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Vendor Retrieve, Update, and Delete API
    
class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


        
# Purchase Order Update and Delete API
class PurchaseOrderUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    

# Vendor Performance List API
class VendorPerformenceView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer



from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView


# Purchase Order Create API
class PurchaseOrderCreate(CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderCreateSerializer

    def create(self, request, *args, **kwargs):
        # Access request data
        request_data = request.data  
        vendor_id = request_data.get('vendor')
        request_data['vendor'] = get_object_or_404(Vendor, id=vendor_id) 
        vendor = request_data['vendor']
        serializer = self.get_serializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(vendor=vendor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
       
from rest_framework.permissions import IsAuthenticated
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework.generics import ListAPIView



# Purchase Order List for Vendor API
class PurchaseOrderListForVendor(ListAPIView):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
      
        vendor = get_object_or_404(Vendor, uid=user.id)
        
        queryset = PurchaseOrder.objects.filter(vendor=vendor.id)
        return queryset
    

# Purchase Order List
class PurchaseOrderListForAdmin(ListAPIView):
    serializer_class = PurchaseOrderSerializer
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Select related field frm vendor model
        queryset = PurchaseOrder.objects.select_related('vendor').all()
        return queryset
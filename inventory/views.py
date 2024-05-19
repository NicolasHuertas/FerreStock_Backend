from django.shortcuts import render
from rest_framework import generics, permissions, status, serializers
from rest_framework.views import APIView
from .models import CustomUser, Order, Product,Supplier
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import (  
    CustomUserSerializer, CustomTokenObtainPairSerializer,
    ProductSerializer, ViewCustomUserSerializer,SupplierSerializer, OrderSerializer, OrderItemSerializer,ViewOrderSerializer,
    ViewOrderProductSerializer
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

    
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.
class CreateCustomUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Obtener el token de autenticaciÃ³n del usuario
            token = request.user.auth_token
            
            # Eliminar el token de la base de datos
            token.delete()

            return JsonResponse({'success': 'Logout successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomUserListView(generics.ListCreateAPIView):
    serializer_class = ViewCustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id:
            return CustomUser.objects.filter(id=user_id)
        else:
            return CustomUser.objects.all()
    
class ProductListUsersView(generics.ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id:
            return Product.objects.filter(user=user_id)
        else:
            return Product.objects.all()

        
class SupplierCreateAPIView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
class SuppllierUpdateAPIView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SuppllierListAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        order_items_data = self.request.data.get('items')
        for item_data in order_items_data:
            product = Product.objects.get(id=item_data['product'])
            if product.user.id != self.request.user.id:
                raise ValidationError('User ID does not match')
            item_data['order'] = order.id
            item_serializer = OrderItemSerializer(data=item_data)
            if item_serializer.is_valid(raise_exception=True):
                item_serializer.save()

class OrderListView(generics.ListAPIView):
    serializer_class = ViewOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status')
        supplier = self.request.query_params.get('supplier')
        order_id = self.request.query_params.get('id')

        if status:
            queryset = queryset.filter(status=status)

        if supplier:
            queryset = queryset.filter(supplier__id=supplier)

        if order_id:
            queryset = queryset.filter(id=order_id)

        return queryset
    
class UpdateOrderStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'message': 'Order ID no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'message': 'Orden no encontrada o no tienes permisos para acceder a esta orden.'}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'Pendiente':
            order.status = 'Entregado'
            order.save()
            return Response({'message': 'Order status actualizada a Entregado'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Order status no está pendiente, no se hicieron cambios'}, status=status.HTTP_200_OK)


class UpdateProductStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        is_pending = request.data.get('is_pending')
        quantity = request.data.get('quantity')

        if not product_id:
            return Response({'message': 'Product ID no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not quantity:
            return Response({'message': 'Quantity no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'message': 'Quantity debe ser un número entero'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)


        if is_pending == 'true':
            product.pending_stock += quantity
        else:
            if product.pending_stock >= quantity:
                product.pending_stock -= quantity
                product.stock += quantity
            else:
                return Response({'message': 'Stock pendiente insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
            
            
        product.save()
        
        return Response({'message': 'Product status Pending actualizada'}, status=status.HTTP_200_OK)
        
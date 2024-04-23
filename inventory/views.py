from django.shortcuts import render
from rest_framework import generics, permissions, status, serializers
from rest_framework.views import APIView
from .models import CustomUser, Product
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import (  
    CustomUserSerializer, 
    ProductSerializer
)



# Create your views here.
class CreateCustomUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.AllowAny]

    #def get_queryset(self):
    #    return Product.objects.filter(user=self.request.user)

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

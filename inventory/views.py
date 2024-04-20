from django.shortcuts import render
from rest_framework import generics, permissions, status, serializers
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import (  
    CustomUserSerializer, 
)



# Create your views here.
class CreateCustomUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


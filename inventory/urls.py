from django.urls import path
from .views import MyTokenObtainPairView, CreateCustomUserView,CustomAuthToken,LogoutView,ProductView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name='inventory'

urlpatterns = [    
   path('create/', CreateCustomUserView.as_view(), name='create_a_new_CustomUser'),
   path('api/token/', CustomAuthToken.as_view(), name='auth_token'),
   path('api/logout/', LogoutView.as_view(), name='logout'),
   path('products/', ProductView.as_view(), name='product-list')
]
from django.urls import path
from .views import MyTokenObtainPairView, CreateCustomUserView,CustomAuthToken,LogoutView,ProductListView,ProductDetailView
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
   path('products/', ProductListView.as_view(), name='product-list'),
   path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail')
]
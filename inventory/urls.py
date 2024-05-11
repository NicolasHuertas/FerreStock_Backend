from django.urls import path
from .views import (MyTokenObtainPairView, CreateCustomUserView,CustomAuthToken,
                    LogoutView,ProductListView,ProductDetailView,CustomUserListView,ProductListUsersView,SupplierCreateAPIView,SuppllierUpdateAPIView)
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

   path('products/', ProductListView.as_view(), name='product-list'),##GET muestra la lista de productos de la sede loggeada - POST crea un producto
   path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),

   path('users/', CustomUserListView.as_view(), name='customuser-list'),##GET obtiene las sedes registradas
   path('products/users/', ProductListUsersView.as_view(), name='product-users-list'),##GET para obtener la lista de los productos sin importar la sede o filtrando por sede
   path('supplier/register/', SupplierCreateAPIView.as_view(), name='supplier-reg'),
   path('supplier/<int:pk>/edit/', SuppllierUpdateAPIView.as_view(), name='supplier-edit'),
]
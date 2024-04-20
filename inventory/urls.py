from django.urls import path
from . import views


app_name='inventory'

urlpatterns = [    
   path('create/', views.CreateCustomUserView.as_view(), name='create_a_new_CustomUser'),
]
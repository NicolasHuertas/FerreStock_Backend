from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, address, contact, manager, nit="763187336", **extra_fields):
        # Create and save a new user with the given email and password
        validate_password(password)
        
        user = self.model(username= username, email=self.normalize_email(email), address=address, contact=contact, manager=manager,  nit=nit, **extra_fields)
        user.set_password(password)
        user.save()   
        
        return user

    def create_superuser(self, username, email, password, address, contact, manager, nit="763187336",**extra_fields):
        # Create and save a new superuser with the given email and password
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                address=address,
                                contact=contact,
                                manager=manager,
                                nit=nit,
                                **extra_fields
                                )
        
        return user


class CustomUser(AbstractUser):

    first_name = None
    last_name = None
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)    
    email = models.EmailField(unique=True, blank=False, null=False) 
    password = models.CharField(max_length=200, validators=[validators.MinLengthValidator(8)])
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    nit = models.CharField(max_length=20, blank=True, default="763187336")
    manager = models.CharField(max_length=30, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = "email"
    #password is always required by default
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f'user email: {self.email} \n username:{self.username}'

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    stock = models.PositiveIntegerField(blank=False, null=False)
    pending_stock = models.PositiveIntegerField(default=0, blank=True) #Unidades vendidas pero no entregadas
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #thumbnail = models.ImageField(aaaaaaaaa)


    def __str__(self):
        return f'User ID: {self.user} \n Product name: {self.name} \n Price: {self.price} \n Stock: {self.stock}'
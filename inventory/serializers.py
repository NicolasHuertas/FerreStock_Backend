from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser, Product,Supplier
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):    
    
    class Meta:
        model = CustomUser
        fields = ['id',
                  'username',
                  'email',
                  'password', 
                  'address',
                  'contact',
                  'nit',
                  'manager'
                 ]        
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'nit': {'required': False}
             }
        
        
    def create(self, validated_data):
        password = validated_data.pop('password')

        try:
            user = CustomUser.objects.create_user(password=password, **validated_data)

        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Customize token payload here
        token['username'] = user.username
        return token


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True},
                        'user': {'read_only': True}
                        }
        

class ViewCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',
                  'username',
                  'email', 
                  'address',
                  'contact',
                  'manager'
                 ]
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'email': {'read_only': True},
            'address': {'read_only': True},
            'contact': {'read_only': True},
            'manager': {'read_only': True},
             }
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'company_name', 'contact_name','address', 'tel', 'email']
          
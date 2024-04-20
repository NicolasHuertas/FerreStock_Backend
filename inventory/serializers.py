from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser


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
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser, Product,Supplier, Order, OrderItem
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

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']         
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    supplier = SupplierSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        
#['user', 'date', 'status', 'supplier']



class ViewOrderSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'company_name', 'email']

class ViewOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']
    
class ViewOrderItemSerializer(serializers.ModelSerializer):
    product = ViewOrderProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class ViewOrderSerializer(serializers.ModelSerializer):
    items = ViewOrderItemSerializer(many=True, read_only=True)
    supplier = ViewOrderSupplierSerializer(read_only=True)
    id_order = serializers.IntegerField(source='id')

    class Meta:
        model = Order
        fields = ['id_order','user', 'date', 'status', 'supplier', 'items']


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderUpdateSerializer(serializers.ModelSerializer):
    items = OrderItemUpdateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'items']

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        order = super().update(instance, validated_data)

        existing_items = instance.items.all()
        existing_items.delete()

        for item_data in items_data:
            product = Product.objects.get(id=item_data['product'])
            if product.user != self.context['request'].user:
                raise ValidationError('User does not match')
            item_data['order'] = order.id
            item_serializer = OrderItemUpdateSerializer(data=item_data)
            if item_serializer.is_valid(raise_exception=True):
                item_serializer.save()

        return order

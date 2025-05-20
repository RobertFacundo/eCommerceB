from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Product, Cart, CartItem
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data.get('email')
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            # Obtener el usuario por nombre de usuario
            user = get_user_model().objects.get(username=data['username'])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        # Verificar la contraseña del usuario
        if user and user.check_password(data['password']):
            # Crear o recuperar el token
            token, created = Token.objects.get_or_create(user=user)

            cart = Cart.objects.filter(user=user).first()
            cart_data = CartSerializer(cart).data if cart else None

            return {
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'cart': cart_data
            }
        else:
            raise serializers.ValidationError('Invalid credentials')
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total']

    def get_total(self, obj):
        return obj.total()


from rest_framework import viewsets
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartItemSerializer, CartSerializer
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

# Create your views here.
def home(request):
    htmlContent = """
        <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #f4f4f4;">
        <div style="background: white; border-radius: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); padding: 30px; max-width: 600px; width: 100%; text-align: center;">
          <p style="font-size: 20px; color: #333; margin-bottom: 20px; font-weight: bold;">
            ⚠️ <strong style="color: #e74c3c;">This backend is hosted for FREE on Render</strong> and may take a few seconds to respond due to cold start.
          </p>
          <p style="font-size: 18px; color: #555; margin-bottom: 20px; font-weight: bold;">
            Now that we know the backend is up and running, feel free to visit the website:
          </p>
          <a href="https://ecommercef-five.vercel.app/" target="_blank" 
             style="font-size: 18px; color: #3498db; text-decoration: none; font-weight: bold; padding: 10px 20px; background-color: #ecf0f1; border-radius: 5px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
            👉 Go to the website
          </a>
          <p style="font-size: 16px; color: #777; margin-top: 20px;">
            Thank you for your patience and understanding!
          </p>
        </div>
    </div>
    """
    return HttpResponse(htmlContent)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Cart.objects.create(user=user)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'token': serializer.validated_data['token']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        else:
            return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def add_product(self, request): 
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
            cart = request.user.cart

            if not cart:
                return Response({"details":"Cart not found"}, status=status.HTTP_404_NOT_FOUND)

            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not item_created:
                cart_item.quantity += int(quantity)
                cart_item.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response({"detail":"Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
            cart = request.user.cart

            if not cart:
                return Response({"details":"Cart not found"}, status=status.HTTP_404_NOT_FOUND)

            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response({"detail":"Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"detail":"Product not in cart"}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from products.models import Product
from .cart import Cart

from .serializers import CartSerializer, CartAddSerializer, CartItemSerializer

class CartDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = Cart(request)
        data = {
            'items': list(cart),
            'total_price': cart.get_total_price(),
            'total_items': len(cart),
        }
        serializer = CartSerializer(data)
        return Response(serializer.data)
    
class CartAddView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            override = serializer.validated_data['override']

            try:
                product = Product.objects.get(id=product_id, available=True)
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Product not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            cart = Cart(request)
            cart.add(product=product, quantity=quantity, override_quantity=override)

            return Response({
                'message': f'"{product.name}" added to cart.',
                'total_items': len(cart),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CartRemoveView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart(request)
        cart.remove(product)

        return Response({
            'message': f'"{product.name}" removed from cart.',
            'total_items': len(cart),
        }, status=status.HTTP_200_OK)
    
class CartClearView(APIView):
    permission_classes = [AllowAny]
    
    def delete(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)
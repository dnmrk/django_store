from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from cart.cart import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product__category'
        )

class OrderDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product__category'
        )

class OrderCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart(request)

        if len(cart) == 0:
            return Response(
                {'error': 'Your cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Charge the price the product has *now*, not the price frozen in
            # the session when it was added to the cart.
            with transaction.atomic():
                order = serializer.save(user=request.user)

                for item in cart:
                    product = item.get('product')
                    if product is None:
                        continue
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=product.price,
                    )

            cart.clear()

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
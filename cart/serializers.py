from rest_framework import serializers
from products.serializers import ProductListSerializer

class CartItemSerializer(serializers.Serializer):
    product = ProductListSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.FloatField(read_only=True)

class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    override = serializers.BooleanField(default=False)

class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.FloatField()
    total_items = serializers.IntegerField()
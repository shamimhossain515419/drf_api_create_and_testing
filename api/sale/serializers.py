# api/sales/serializers.py

from rest_framework import serializers
from .models import Sale, SaleItem
from api.products.models import Product


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = SaleItem
        fields = ["id", "product", "product_name", "quantity", "price_at_sale"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Sale
        fields = ["id", "user_name", "created_at", "total_amount", "items"]

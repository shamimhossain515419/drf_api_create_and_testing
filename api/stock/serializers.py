# serializers.py
from rest_framework import serializers
from api.products.serializers import ProductSerializer
from api.products.models import Product
from api.stock.models import Stock


class StockSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id",
            "product",
            "product_id",
            "user",
            "product_name",
            "quantity",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

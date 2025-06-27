from django.shortcuts import render
from api.stock.serializers import StockSerializer
from api.stock.models import Stock
from rest_framework import viewsets, permissions


# Create your views here.
# views.py
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by("-created_at")
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        user = self.request.user

        existing_stock = Stock.objects.filter(product=product, user=user).first()

        if existing_stock:
            # Update the quantity
            existing_stock.quantity += serializer.validated_data["quantity"]
            existing_stock.save()
        else:
            # Create new stock
            serializer.save(user=user)

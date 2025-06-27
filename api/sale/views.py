from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from api.sale.models import Sale, SaleItem
from api.sale.serializers import SaleSerializer
from api.stock.models import Stock


class SaleCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user

        items_data = data.get("items", [])
        if not items_data:
            return Response({"message": "No sale items provided."}, status=400)

        # Create Sale first (so SaleItem FK can use it)
        sale = Sale.objects.create(user=user)
        total = 0

        for item in items_data:
            product_id = item.get("product")
            quantity = int(item.get("quantity", 0))
            price_at_sale = float(item.get("price_at_sale", 0))

            if not product_id or quantity <= 0:
                return Response({"message": "Invalid product or quantity."}, status=400)

            try:
                stock = Stock.objects.select_related("product").get(
                    product_id=product_id
                )
                product = stock.product
            except Stock.DoesNotExist:
                return Response(
                    {"message": f"Stock not found for Product ID {product_id}."},
                    status=404,
                )

            if stock.quantity < quantity:
                return Response(
                    {
                        "message": f"Not enough stock for product '{product.name}'. Available: {stock.quantity}"
                    },
                    status=400,
                )

            # Reduce stock
            stock.quantity -= quantity
            stock.save()

            # Create SaleItem
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price_at_sale=price_at_sale,
            )

            total += price_at_sale * quantity

        sale.total_amount = total
        sale.save()

        return Response(SaleSerializer(sale).data, status=status.HTTP_201_CREATED)

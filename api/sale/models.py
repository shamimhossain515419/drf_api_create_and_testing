from django.db import models
from api.products.models import Product
from django.contrib.auth.models import User  # or your custom user model


# Create your models here.
class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sale {self.id} - {self.sale.username}"

    class Meta:
        db_table = "sales"
        ordering = ["-created_at"]


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Must be added

    def get_total(self):
        return self.quantity * self.price_at_sale

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        db_table = "sale_items"
        ordering = ["-created_at"]  # ✅ Now this will work

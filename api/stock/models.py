from django.db import models
from api.products.models import Product
from django.contrib.auth.models import User  # অথবা custom user ব্যবহার করলে সেটি

# Create your models here.


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="stocked_products"
    )
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ["product__name"]

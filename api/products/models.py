from django.db import models

# Create your models here.
from django.contrib.auth.models import User  # or your custom user model


class Product(models.Model):
    name = models.CharField(max_length=255)
    added = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

from django.contrib.auth.models import User
from django.db import models
from api.blog_category.models import BlogCategory


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE, related_name="blogs", null=True
    )
    added = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blogs", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blogs"
        ordering = ["-created_at"]

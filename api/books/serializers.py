from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_title(self, value):
        if Book.objects.filter(title=value).exists():
            raise serializers.ValidationError("This title is already taken.")
        return value

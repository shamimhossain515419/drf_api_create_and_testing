from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()  # override

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "slug",
            "category_id",
            "added_id",
            "category",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_category(self, obj):
        return obj.category.name if obj.category else None

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

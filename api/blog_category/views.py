from rest_framework import viewsets, filters
from rest_framework.response import Response
from api.blog_category.serializers import BlogCategorySerializer
from .models import BlogCategory
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogCategoryClassApiView(APIView):
    def get(self, request, slug):
        queryset = BlogCategory.objects.filter(slug=slug)
        if not queryset.exists():
            return Response(
                {"detail": "Blog category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BlogCategorySerializer(queryset, many=True)
        return Response(serializer.data)

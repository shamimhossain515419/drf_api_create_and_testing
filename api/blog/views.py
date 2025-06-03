from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.blog.serializers import BlogSerializer
from api.blog_category.models import BlogCategory
from api.blog.models import Blog
from django.db.models import Q
from rest_framework.generics import get_object_or_404


# Create your views here.
class BlogCreateListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        category_id = request.data.get("category_id")

        if not category_id:
            return Response(
                {"error": "Category ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if category exists
        if not BlogCategory.objects.filter(id=category_id).exists():
            return Response(
                {"error": "Invalid category ID. Category does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["added_id"] = request.user.id

        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        blogs = Blog.objects.filter(added_id=request.user)
        search_query = request.query_params.get("search")
        field_query = request.query_params.get("fields")

        if search_query:
            blogs = blogs.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

            # Convert field_query to list
        if field_query:
            requested_fields = [f.strip() for f in field_query.split(",")]
        else:
            requested_fields = None  # Default to all

        serializer = BlogSerializer(blogs, many=True, fields=requested_fields)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Blog updated successfully.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, added_id=request.user)
        serializer = BlogSerializer(blog)
        return Response(
            {"message": "Blog fetched successfully.", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, added_id=request.user)
        blog.delete()
        return Response(
            {"message": "Blog deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

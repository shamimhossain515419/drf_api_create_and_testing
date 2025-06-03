from django.urls import path
from api.blog.views import BlogCreateListApiView, BlogDetailApiView

urlpatterns = [
    path("", BlogCreateListApiView.as_view(), name="blog-create-list"),
    path("<int:pk>/", BlogDetailApiView.as_view(), name="blog-detail-delete"),
]

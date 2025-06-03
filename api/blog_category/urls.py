from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.blog_category.views import BlogCategoryClassApiView
from .views import BlogCategoryViewSet

router = DefaultRouter()
router.register(r"", BlogCategoryViewSet, basename="blog-category")
urlpatterns = [
    path(
        "by-slug/<slug:slug>/",
        BlogCategoryClassApiView.as_view(),
        name="blog-category-list",
    ),
    path("", include(router.urls)),
]

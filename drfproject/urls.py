from django.contrib import admin
from django.urls import path, include
from api.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("api.books.urls")),
    path("api/cars/", include("api.cars.urls")),
    path("api/auth/", include("api.authapi.urls")),
    path("api/blog-category/", include("api.blog_category.urls")),
    path("api/blog/", include("api.blog.urls")),
    path("api/products/", include("api.products.urls")),
    path("api/stock/", include("api.stock.urls")),
    path("api/sale/", include("api.sale.urls")),
    path("", home),
]

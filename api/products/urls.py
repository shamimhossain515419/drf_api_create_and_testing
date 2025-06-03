from django.urls import path
from api.products.views import ProductListCreateView, ProductRetrieveUpdateDestroyView

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="product-list-create"),
    path(
        "<int:pk>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="product-detail",
    ),
]

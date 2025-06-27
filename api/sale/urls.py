# api/sales/urls.py

from django.urls import path
from api.sale.views import SaleCreateView

urlpatterns = [
    path("create/", SaleCreateView.as_view(), name="sale-create"),
]

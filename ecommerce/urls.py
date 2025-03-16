from django.urls import path
from .views import print_invoice_view

app_name = "ecommerce"

urlpatterns = [
    path("invoice/<int:invoice_id>/print/", print_invoice_view, name="print_invoice"),
]

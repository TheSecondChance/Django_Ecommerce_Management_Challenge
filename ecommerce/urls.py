from django.urls import path
from .views import print_invoice_view, sales_dashboard

app_name = "ecommerce"

urlpatterns = [
    path("invoice/<int:invoice_id>/print/", print_invoice_view, name="print_invoice"),
    path("sales-dashboard/", sales_dashboard, name="sales_dashboard"),
]

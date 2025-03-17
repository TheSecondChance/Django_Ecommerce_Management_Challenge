from django.utils.timezone import now
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404
from .models import Invoice, InvoiceLineItem, PurchaseOrder


def print_invoice_view(request, invoice_id):
    invoice = get_object_or_404(
        Invoice.objects.annotate(
            total=Sum(F("line_items__quantity") * F("line_items__price_each"))
        ),
        id=invoice_id,
    )
    return render(request, "admin/print_invoice.html", {"invoice": invoice})


def sales_dashboard(request):
    """
    Renders the sales dashboard with key business metrics.

    This view calculates and provides the following insights:

    - Top-selling products: Retrieves the top 3 products based on total quantity sold.
    - Overdue invoices: Lists invoices above $500 that are unpaid and past their due date.
    - Total purchase cost per vendor: Aggregates the total amount spent per vendor.
    - Top customers: Identifies customers who have spent the most based on invoice totals.

    The computed data is passed to the 'sales_dashboard.html' template for display.
    
    You can access this dashboard at:
    http://127.0.0.1:8000/ecommerce/sales-dashboard/
    """
    sales_per_product = (
        InvoiceLineItem.objects.values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:3]
    )

    overdue_invoices = Invoice.objects.annotate(
        total=Sum(F("line_items__quantity") * F("line_items__price_each"))
    ).filter(total__gt=500, is_paid=False, invoice_date__lt=now().date())

    vendor_totals = PurchaseOrder.objects.values("vendor_name").annotate(
        total_spent=Sum(F("line_items__quantity") * F("line_items__cost_per_unit"))
    )

    top_customers = (
        Invoice.objects.values("customer_name")
        .annotate(
            total_spent=Sum(F("line_items__quantity") * F("line_items__price_each"))
        )
        .order_by("-total_spent")
    )

    context = {
        "sales_per_product": sales_per_product,
        "overdue_invoices": overdue_invoices,
        "vendor_totals": vendor_totals,
        "top_customers": top_customers,
    }

    return render(request, "ecommerce/sales_dashboard.html", context)

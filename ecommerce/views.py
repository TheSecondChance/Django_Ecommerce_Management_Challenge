from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, F
from .models import Invoice


def print_invoice_view(request, invoice_id):
    invoice = get_object_or_404(
        Invoice.objects.annotate(
            total=Sum(F("line_items__quantity") * F("line_items__price_each"))
        ),
        id=invoice_id,
    )
    return render(request, "admin/print_invoice.html", {"invoice": invoice})

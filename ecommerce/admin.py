from django.contrib import admin, messages
from django.utils.html import format_html
from django.db.models import Sum, F, Case, When, BooleanField
from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from .models import (
    Product,
    PurchaseOrder,
    PurchaseOrderLineItem,
    Invoice,
    InvoiceLineItem,
)

admin.site.register(Product)


class PurchaseOrderLineItemInline(admin.TabularInline):
    model = PurchaseOrderLineItem
    extra = 1
    readonly_fields = ("line_total",)

    def line_total(self, instance):
        return f"${instance.total_cost():.2f}"

    line_total.short_description = "Line Total"


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("vendor_name", "order_date", "status", "calculated_total")
    inlines = [PurchaseOrderLineItemInline]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                total=Sum(F("line_items__quantity") * F("line_items__cost_per_unit"))
            )
        )

    def calculated_total(self, obj):
        return f"${obj.total:,.2f}" if hasattr(obj, "total") else "N/A"

    calculated_total.short_description = "Total Cost"
    calculated_total.admin_order_field = "total"


class InvoiceLineItemInline(admin.TabularInline):
    model = InvoiceLineItem
    extra = 1
    readonly_fields = ("line_total",)

    def line_total(self, instance):
        return f"${instance.total_price():.2f}" if instance.total_price() else "N/A"

    line_total.short_description = "Line Total"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "invoice_date",
        "colored_status",
        "calculated_total",
    )
    list_filter = ("is_paid",)
    inlines = [InvoiceLineItemInline]
    actions = ["mark_as_paid", "export_invoice_to_xlsx"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                total=Sum(F("line_items__quantity") * F("line_items__price_each")),
                is_overdue=Case(
                    When(
                        invoice_date__lt=timezone.now().date(),
                        is_paid=False,
                        then=True,
                    ),
                    default=False,
                    output_field=BooleanField(),
                ),
            )
        )

    def colored_status(self, obj):
        if obj.is_paid:
            return format_html('<span style="color: green;">✓ Paid</span>')
        if obj.is_overdue:
            return format_html('<span style="color: red;">⬤ Overdue</span>')
        return format_html('<span style="color: orange;">⌛ On Time</span>')

    colored_status.short_description = "Payment Status"

    def calculated_total(self, obj):
        return f"${obj.total:,.2f}" if hasattr(obj, "total") else "N/A"

    calculated_total.short_description = "Total Price"
    calculated_total.admin_order_field = "total"

    @admin.action(description="Mark selected invoices as paid")
    def mark_as_paid(self, request, queryset):
        updated_count = queryset.filter(is_paid=False).update(is_paid=True)
        if updated_count:
            self.message_user(
                request,
                f"Successfully marked {updated_count} invoice(s) as paid.",
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                "No invoices were updated. They might already be marked as paid.",
                messages.WARNING,
            )

    @admin.action(description="Export to Excel")
    def export_invoice_to_xlsx(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "Invoices"
        ws.append(
            [
                "Invoice ID",
                "Customer",
                "Date",
                "Status",
                "Product",
                "Quantity",
                "Unit Price",
                "Total",
            ]
        )

        for invoice in queryset.prefetch_related("line_items"):
            for item in invoice.line_items.all():
                ws.append(
                    [
                        invoice.id,
                        invoice.customer_name,
                        invoice.invoice_date,
                        (
                            "Paid"
                            if invoice.is_paid
                            else "Overdue" if invoice.is_overdue else "Pending"
                        ),
                        item.product.name,
                        item.quantity,
                        item.price_each,
                        item.total_price(),
                    ]
                )

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=invoices.xlsx"
        wb.save(response)
        return response

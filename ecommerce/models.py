from django.db import models
from django.db.models import Sum, F
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    vendor_name = models.CharField(max_length=255)
    order_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def total_cost(self):
        return (
            self.line_items.aggregate(total=Sum(F("quantity") * F("cost_per_unit")))[
                "total"
            ]
            or 0
        )

    def __str__(self):
        return self.vendor_name


class PurchaseOrderLineItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="line_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def total_cost(self):
        if self.quantity is None or self.cost_per_unit is None:
            return 0
        return self.quantity * self.cost_per_unit

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Invoice(models.Model):
    customer_name = models.CharField(max_length=255)
    invoice_date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def is_overdue(self):
        return not self.is_paid and self.invoice_date < timezone.now().date()

    def total_price(self):
        return (
            self.line_items.aggregate(total=Sum(F("quantity") * F("price_each")))[
                "total"
            ]
            or 0
        )

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name}"


class InvoiceLineItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="line_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_each = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        if self.quantity is None or self.price_each is None:
            return 0
        return self.quantity * self.price_each

    def __str__(self):
        return f"{self.product.name} x {self.quantity if self.quantity else 0}"

from django.test import TestCase
from django.utils import timezone
from .models import (
    Product,
    PurchaseOrder,
    PurchaseOrderLineItem,
    Invoice,
    InvoiceLineItem,
)


class ECommerceModelsTest(TestCase):
    def setUp(self):
        """Create test data for all models."""
        self.product = Product.objects.create(
            name="Test Product", sku="SKU123", unit_price=10.00
        )

        self.purchase_order = PurchaseOrder.objects.create(vendor_name="Test Vendor")
        self.purchase_line_item = PurchaseOrderLineItem.objects.create(
            purchase_order=self.purchase_order,
            product=self.product,
            quantity=5,
            cost_per_unit=8.00,
        )

        self.invoice = Invoice.objects.create(
            customer_name="John Doe", invoice_date=timezone.now().date()
        )
        self.invoice_line_item = InvoiceLineItem.objects.create(
            invoice=self.invoice, product=self.product, quantity=3, price_each=12.00
        )

    def test_product_creation(self):
        """Test if product is created correctly."""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.sku, "SKU123")
        self.assertEqual(float(self.product.unit_price), 10.00)

    def test_purchase_order_total_cost(self):
        """Test if the total cost of a purchase order is calculated correctly."""
        self.assertEqual(float(self.purchase_order.total_cost()), 40.00)

    def test_invoice_total_price(self):
        """Test if the total price of an invoice is calculated correctly."""
        self.assertEqual(float(self.invoice.total_price()), 36.00)

    def test_invoice_overdue(self):
        """Test if an invoice is correctly marked as overdue."""
        self.assertFalse(self.invoice.is_overdue())
        self.invoice.invoice_date = timezone.now().date() - timezone.timedelta(days=2)
        self.assertTrue(self.invoice.is_overdue())

    def test_purchase_line_item_total_cost(self):
        """Test line item cost calculation."""
        self.assertEqual(float(self.purchase_line_item.total_cost()), 40.00)

    def test_invoice_line_item_total_price(self):
        """Test line item price calculation."""
        self.assertEqual(
            float(self.invoice_line_item.total_price()), 36.00
        )

Requirements

1. Models
   ○ Product: Holds name, sku, unit_price, etc.

   ○ PurchaseOrder: Contains info about the vendor, order date, status.
   Must link to Product via a line item model (e.g., PurchaseOrderLineItem) that tracks
   quantity, cost, etc.

   ○ Invoice: Represents a customer invoice, linking to one or more Products via a
   line item model (e.g., InvoiceLineItem with quantity, price).

   ○ InvoiceLineItem (or equivalent): Associates an Invoice with a Product,
   storing fields like quantity, price_each.

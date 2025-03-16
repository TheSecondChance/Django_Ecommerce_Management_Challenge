# Ecommerce_Management

This project is a Django-based system for managing invoices and purchase orders. It provides an admin panel with customized features such as inline editing, calculated fields, custom actions, and advanced ORM queries.

## Features

- **Admin Customization**

  - Display calculated totals for invoices and purchase orders.
  - Inline editing of line items.
  - Custom admin actions (e.g., marking invoices as paid).
  - Custom HTML and widget overrides (e.g., highlighting overdue invoices).
  - Export invoices as an XLSX file.

- **Advanced ORM Queries**
  - Annotate totals (e.g., total cost/price) on models.
  - Filter or group results based on annotated fields.
  - Conditional queries for overdue invoices above a certain amount.
  - Reports for top-selling products, top customers, and vendor totals.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/TheSecondChance/Django_Ecommerce_Management_Challenge.git

   cd Django_Ecommerce_Management_Challenge
   ```

2. Create a virtual environment and install dependencies:

   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Apply migrations and create a superuser:

   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Run the development server:

   ```sh
   python manage.py runserver
   ```

5. Access the admin panel at:
   ```
   http://127.0.0.1:8000/admin/
   ```

## Code Formatting

This project uses `black` for Python formatting. To format your code, run:

```sh
black file_name.py
```

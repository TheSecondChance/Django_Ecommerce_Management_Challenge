# Generated by Django 5.1.7 on 2025-03-16 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ecommerce", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoice",
            name="due_date",
        ),
    ]

# Generated by Django 3.2 on 2021-04-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_remove_stock_current_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockreminder',
            name='lower',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockreminder',
            name='upper',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

# Generated by Django 3.2 on 2021-04-30 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("stock", "0003_auto_20210430_1452")]

    operations = [
        migrations.AlterField(
            model_name="stockreminder",
            name="periods",
            field=models.ManyToManyField(blank=True, null=True, to="stock.Period"),
        )
    ]

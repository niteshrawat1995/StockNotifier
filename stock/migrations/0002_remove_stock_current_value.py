# Generated by Django 3.2 on 2021-04-30 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("stock", "0001_initial")]

    operations = [migrations.RemoveField(model_name="stock", name="current_value")]

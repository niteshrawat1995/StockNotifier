# Generated by Django 3.2 on 2021-04-30 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("account", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(default=7503437728, max_length=10, unique=True),
            preserve_default=False,
        )
    ]

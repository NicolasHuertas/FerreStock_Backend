# Generated by Django 4.2.6 on 2024-05-19 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_pending',
            field=models.BooleanField(default=False),
        ),
    ]

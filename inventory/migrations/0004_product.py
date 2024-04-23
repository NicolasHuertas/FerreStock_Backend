# Generated by Django 4.2.6 on 2024-04-21 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_rename_direccion_customuser_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('stock', models.PositiveIntegerField()),
                ('pending_stock', models.PositiveIntegerField(blank=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
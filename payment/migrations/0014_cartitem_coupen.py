# Generated by Django 5.0 on 2024-01-27 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0004_coupon'),
        ('payment', '0013_cartorder_coupen'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='coupen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminhome.coupon'),
        ),
    ]
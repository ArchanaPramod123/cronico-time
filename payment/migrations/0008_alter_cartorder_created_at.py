# Generated by Django 5.0 on 2024-01-08 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_cartorder_created_at_alter_cartorder_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

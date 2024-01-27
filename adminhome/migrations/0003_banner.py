# Generated by Django 5.0 on 2024-01-27 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0002_remove_productoffer_discount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='banners/')),
                ('description1', models.TextField(blank=True, null=True)),
                ('description2', models.TextField(blank=True, null=True)),
                ('description3', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
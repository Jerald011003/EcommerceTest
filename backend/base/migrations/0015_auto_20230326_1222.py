# Generated by Django 3.1.4 on 2023-03-26 04:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20230326_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
        ),
    ]

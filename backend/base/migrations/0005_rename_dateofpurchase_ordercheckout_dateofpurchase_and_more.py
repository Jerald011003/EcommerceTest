# Generated by Django 4.1.5 on 2023-02-04 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_ordercheckout_purchasedgame_alter_orderitem_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordercheckout',
            old_name='dateofpurchase',
            new_name='dateofPurchase',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shippingPrice',
        ),
    ]

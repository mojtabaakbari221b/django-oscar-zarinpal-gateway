# Generated by Django 3.2.12 on 2022-03-12 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_alter_zarrinpaytransaction_shipping_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zarrinpaytransaction',
            name='shipping_address',
        ),
    ]

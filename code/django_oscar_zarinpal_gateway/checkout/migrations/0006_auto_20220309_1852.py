# Generated by Django 3.2.12 on 2022-03-09 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_alter_zarrinpaytransaction_pay_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='zarrinpaytransaction',
            name='billing_address_class',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zarrinpaytransaction',
            name='billing_address_module',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zarrinpaytransaction',
            name='shipping_address_class',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zarrinpaytransaction',
            name='shipping_address_module',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zarrinpaytransaction',
            name='shipping_method_class',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zarrinpaytransaction',
            name='shipping_method_module',
            field=models.TextField(blank=True, null=True),
        ),
    ]

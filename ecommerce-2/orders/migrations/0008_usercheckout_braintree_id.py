# Generated by Django 2.2 on 2019-04-22 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercheckout',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]

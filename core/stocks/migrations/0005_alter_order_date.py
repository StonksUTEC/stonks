# Generated by Django 4.0.4 on 2022-06-24 22:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_portfolio_avg_price_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 22, 24, 50, 607818, tzinfo=utc)),
        ),
    ]
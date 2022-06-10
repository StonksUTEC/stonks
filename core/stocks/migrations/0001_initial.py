# Generated by Django 4.0.4 on 2022-06-03 23:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('ruc', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('acronym', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('[A-Z]{1,12}', 'Acrónimo inválido')])),
                ('company_name', models.CharField(max_length=64)),
                ('lastest_price', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('client_dni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('company_ruc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.company')),
            ],
            options={
                'unique_together': {('client_dni', 'company_ruc')},
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('transaction_type', models.CharField(choices=[('BM', 'Buy Market'), ('BL', 'Buy Limit'), ('BS', 'Buy Stop'), ('SM', 'Sell Market'), ('SL', 'Sell Limit'), ('SS', 'Sell Stop')], max_length=2)),
                ('client_dni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('company_ruc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.company')),
            ],
        ),
        migrations.CreateModel(
            name='IncompleteOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=1)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.order')),
            ],
        ),
        migrations.CreateModel(
            name='CompleteOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_stock', models.DecimalField(decimal_places=2, max_digits=7)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.order')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='stocks_for_client',
            field=models.ManyToManyField(through='stocks.Portfolio', to=settings.AUTH_USER_MODEL),
        ),
    ]
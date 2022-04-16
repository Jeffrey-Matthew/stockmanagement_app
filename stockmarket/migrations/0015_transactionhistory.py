# Generated by Django 4.0.3 on 2022-04-15 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0014_rename_limitorder_time_limitorders_expiration_dt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='transactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=200)),
                ('action_type', models.CharField(choices=[('LIMIT_ORDER', 'LIMIT_ORDER'), ('CASH', 'CASH')], max_length=200)),
                ('txn_date', models.DateTimeField(null=True)),
                ('stock_name', models.CharField(max_length=200, null=True)),
                ('stock_price', models.FloatField(null=True)),
                ('stock_volumes', models.FloatField(null=True)),
                ('total_amt', models.FloatField(null=True)),
                ('user_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stockmarket.userinfo')),
            ],
        ),
    ]
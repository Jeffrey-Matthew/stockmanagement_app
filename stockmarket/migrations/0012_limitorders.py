# Generated by Django 4.0.3 on 2022-04-15 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0011_user_stock_number_of_volumes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='limitOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limitOrder_type', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=50)),
                ('limitOrder_time', models.DateTimeField(null=True)),
                ('stock_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stockmarket.stock')),
                ('user_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stockmarket.userinfo')),
            ],
        ),
    ]

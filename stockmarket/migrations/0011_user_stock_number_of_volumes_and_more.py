# Generated by Django 4.0.3 on 2022-04-14 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0010_stock_limit_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_stock',
            name='number_of_volumes',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='user_stock',
            name='stock_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

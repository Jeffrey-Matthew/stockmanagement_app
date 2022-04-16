from email.policy import default
from django.db import models

# Create your models here.
class Userinfo(models.Model):
    user_name = models.CharField(max_length=50,null=True)
    full_name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=30,null=True)
    user_created_dt = models.DateTimeField(auto_now_add = True,null=True)
    def __str__(self):
        return self.user_name

class Stock(models.Model):
    stock_name = models.CharField(max_length=200,null=True)
    stock_created_dt = models.DateTimeField(null=True,auto_now=True)
    limit_order_val = models.FloatField(null=True)
    limit_order_date = models.DateTimeField(null=True)
    market_price = models.FloatField(null=True)
    status_choices = (('LIMIT_ORDER_BUY','LIMIT_ORDER_BUY'),('LIMIT_ORDER_SELL','LIMIT_ORDER_SELL'),('BOUGHT','BOUGHT'),
                    ('AVAILABLE','AVAILABLE'))
    status = models.CharField(max_length=200,null=True,choices=status_choices)
    stock_ticker = models.CharField(max_length=5,null=True)
    volumes = models.FloatField(null=True)

    

class User_stock(models.Model):
    user_name = models.ForeignKey(Userinfo,null=True,on_delete=models.SET_NULL)
    stock_name = models.CharField(max_length=200,null=True)
    number_of_volumes = models.FloatField(null=True)
    sold_dt = models.DateTimeField(auto_now_add=True,null=True)

class Stock_history(models.Model):
    user_name = models.ForeignKey(Userinfo,null=True,on_delete=models.SET_NULL)
    stock_name = models.ForeignKey(Stock,null=True,on_delete=models.SET_NULL)
    price_sold = models.FloatField(null=True)
    date = models.DateTimeField(null=True)

class Market(models.Model):
    market_start_time =  models.TimeField(null=True)
    market_end_time = models.TimeField(null=True)
    market_schedule_choices = (('WEEKDAYS_ONLY','WEEKDAYS_ONLY'),('ALL_DAYS','ALL_DAYS'))
    market_schedule = models.CharField(max_length=50,choices=market_schedule_choices)

class Day_trade(models.Model):
    stock_name = models.ForeignKey(Stock,null=True,on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True,null=True)
    high_val = models.FloatField(null=True)
    low_val = models.FloatField(null=True)
    begin_val = models.FloatField(null=True)

class Bank(models.Model):
    user_name = models.ForeignKey(Userinfo,null=True,on_delete=models.SET_NULL)
    cash_available = models.FloatField(null=True)
    user_withdrawal_limit = models.FloatField(null=True,default=500)
    user_deposit_limit = models.FloatField(null=True,default=500)
    withdraw_date = models.DateTimeField(null=True)
    deposit_date = models.DateTimeField(null=True)
    stock_cash = models.FloatField(null=True,default=0)

class limitOrders(models.Model):
    user_name = models.ForeignKey(Userinfo,null=True,on_delete=models.SET_NULL)
    stock_name = models.CharField(max_length=200,null=True)
    limitOrderChoice = (('BUY','BUY'),('SELL','SELL'))
    limitOrder_type = models.CharField(max_length=50,choices=limitOrderChoice)
    expiration_dt = models.DateTimeField(null=True)
    limitOrder_volumes = models.FloatField(null=True)
    limitOrder_price = models.FloatField(null=True)
    created_dt = models.DateTimeField(auto_now=True,null=True)

class transactionHistory(models.Model):
    user_name = models.ForeignKey(Userinfo,null=True,on_delete=models.SET_NULL)
    action_choices = (('BUY','BUY'),('SELL','SELL'))
    action = models.CharField(max_length=200,choices=action_choices)
    action_type_choices = (('LIMIT_ORDER','LIMIT_ORDER'),('CASH','CASH'))
    action_type = models.CharField(max_length=200,choices=action_type_choices)
    txn_date = models.DateTimeField(null=True)
    stock_name = models.CharField(max_length=200,null=True)
    stock_price = models.FloatField(null=True)
    stock_volumes = models.FloatField(null=True)
    total_amt = models.FloatField(null=True)

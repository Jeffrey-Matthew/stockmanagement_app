# Python Code
# myapp/management/commands/mytask.py

from django.core.management.base import BaseCommand, CommandError
from stockmarket.models import *
from random import randint
from stockmarket.utils import *
from stockmarket.views import *

class Command(BaseCommand):
	help = 'Type the help text here'

	def fetchRandomValue(self):
		return randint(-20,5)

	def handleLimitOrders(self):
		limit_order_obj = limitOrders.objects.order_by('-created_dt')
		for limit_order in limit_order_obj:
			if limit_order.limitOrder_type == 'BUY':
				user_name = limit_order.user_name.user_name
				stock_name = limit_order.stock_name
				current_balance = fetchCurrentBalance(user_name=user_name) 
				limit_order_val = limit_order.limitOrder_price 
				curr_stock_price = fetchStockInfo(stock_name)[0]
				if curr_stock_price<=limit_order_val and (current_balance-curr_stock_price>=0):
					buyStock_util(user_name,stock_name,limit_order.limitOrder_volumes,limit_order.limitOrder_price,limitOrder_bool = True)
					del_limit_order = limitOrders.objects.get(id=limit_order.id)
					del_limit_order.delete()
			else:
				user_name = limit_order.user_name.user_name
				stock_name = limit_order.stock_name
				current_balance = fetchCurrentBalance(user_name=user_name) 
				limit_order_val = limit_order.limitOrder_price 
				curr_stock_price = fetchStockInfo(stock_name)[0]
				if curr_stock_price>=limit_order_val and (current_balance+curr_stock_price>=0):
					sellStockUtil(user_name,stock_name,limit_order.limitOrder_volumes,limit_order.limitOrder_price,limitOrder_bool = True)
					del_limit_order = limitOrders.objects.get(id=limit_order.id)
					del_limit_order.delete()
				


	

	def handle(self, *args, **options):
		# Add yout logic here
		# This is the task that will be run
		stocks_obj = Stock.objects.all()
		for stock in stocks_obj:
			current_stock = Stock.objects.get(id=stock.id)
			current_stock_price = current_stock.market_price
			rand_int_value = float(self.fetchRandomValue())
			#print(current_stock_price + rand_int_value)
			while current_stock_price + rand_int_value <= 0:
				rand_int_value = float(self.fetchRandomValue())
			#print(current_stock_price+rand_int_value)
			current_stock.market_price = current_stock_price+rand_int_value
			stock_obj = Day_trade.objects.filter(stock_name=Stock.objects.get(stock_name=stock.stock_name),date=datetime.today())
			if stock_obj:
				stock_obj = Day_trade.objects.get(stock_name=Stock.objects.get(stock_name=stock.stock_name),date=datetime.today())
				if current_stock_price > stock_obj.high_val:
					stock_obj.high_val = current_stock.market_price
				if current_stock.market_price < stock_obj.low_val:
					stock_obj.low_val = current_stock.market_price
				stock_obj.save()
			else:
				new_stock_obj = Day_trade()
				new_stock_obj.stock_name = Stock.objects.get(stock_name=stock.stock_name)
				new_stock_obj.date = datetime.today()
				new_stock_obj.begin_val = current_stock.market_price
				new_stock_obj.high_val = current_stock.market_price
				new_stock_obj.low_val = current_stock.market_price
				new_stock_obj.save()
				current_stock.save()
		self.handleLimitOrders()
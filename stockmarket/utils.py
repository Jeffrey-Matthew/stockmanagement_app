from ast import Try
from cmath import exp

from datetime import datetime
from logging import exception
from .models import *
from .views import *

def fetchcrntMrktSchedule():
	# market_obj = Market.objects.get(id=1)
	# field_name = 'market_start_time'
	# market_field_obj = Market._meta.get_field(field_name)
	# market_strt_time_val = market_field_obj.value_from_object(market_obj)
	
	market_start_time = fetchValuefromDb(Market,'market_start_time',1)
	print('Fetch Method invoked')
	market_end_time = fetchValuefromDb(Market,'market_end_time',1)
	market_schedule = fetchValuefromDb(Market,'market_schedule',1)
	#print(Market.objects.get(id=1).market_start_time)
	return (market_start_time,market_end_time,market_schedule)
	


# If you have the Pkey value and the model as well as field name , return the value present in it.
def fetchValuefromDb(model,field_name,id_val):
	model_obj = model.objects.get(id=id_val)
	field_obj = model._meta.get_field(field_name)
	field_val = field_obj.value_from_object(model_obj)
	return field_val

def checkifStockExists(stock_name):
	stock_obj = Stock.objects.filter(stock_name=stock_name)
	if stock_obj:
		return True 
	return False

def fetchStocksforUser(user_name) -> list :
	pass

def fetchAllStocks():
	stock_obj = Stock.objects.all()
	stock_name_ls = []
	for stock in stock_obj:
		#print(stock.market_price)
		stock_name_ls.append(stock)
	#print(stock_name_ls)
	return stock_name_ls

def fetchStockInfo(stock_name):
	try:
		#print(stock_name)
		stock_obj = Stock.objects.get(stock_name=stock_name)
		print(stock_obj)
		stock_day_obj = Day_trade.objects.filter(stock_name=Stock.objects.get(stock_name=stock_name))
		if stock_day_obj:
			stock_day_obj = Day_trade.objects.get(stock_name=Stock.objects.get(stock_name=stock_name))
			return [stock_obj.market_price,stock_obj.stock_ticker,stock_obj.volumes,stock_obj.market_price*stock_obj.volumes,stock_day_obj.begin_val,stock_day_obj.high_val,stock_day_obj.low_val]
		else:
			return [stock_obj.market_price,stock_obj.stock_ticker,stock_obj.volumes,stock_obj.market_price*stock_obj.volumes,'','','']
	except Exception as e:
		print(e)
		return ['','','','']

def fetchstocks(user_name):
	try:
		User_info = Userinfo.objects.get(user_name=user_name)
		user_stock_obj = User_stock.objects.filter(user_name = User_info)
		#print(user_stock_obj)
		user_stock_info = []
		# for user_stock in user_stock_obj:
		#     new_ls = []
		#     user_stock_info.append([[user_stock.stock_name],[user_stock.number_of_volumes]])
		# print(user_stock_info)
		return user_stock_obj
	except Exception as e:
		print(e)
		return []

def buyStock_util(user_name,stock_name,number_of_volumes,stock_market_price,limitOrder_bool):

	User_info = Userinfo.objects.get(user_name=user_name)
	user_stock_obj = User_stock.objects.filter(user_name=User_info,stock_name=stock_name)
	if not limitOrder_bool:
		stock_market_price = fetchStockInfo(stock_name)[0] * float(number_of_volumes)
	if user_stock_obj:
		user_stock_obj = User_stock.objects.get(user_name=User_info,stock_name=stock_name)
		user_stock_obj.user_name = User_info
		user_stock_obj.stock_name = stock_name
		user_stock_obj.number_of_volumes+= float(number_of_volumes)
		
		user_stock_obj.save()
	else:
		new_stock = User_stock()
		new_stock.user_name = User_info
		new_stock.stock_name = stock_name
		new_stock.number_of_volumes = float(number_of_volumes)
		new_stock.save()
	login_user_name = str(user_name) 
	login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
	bank_obj = Bank.objects.get(user_name=login_user_info_obj)   
	bank_obj.cash_available-= stock_market_price
	bank_obj.save()
	stock_obj = Stock.objects.get(stock_name=stock_name)
	stock_obj.volumes-=float(number_of_volumes)
	stock_obj.save()
	addTransaction(user_name,'BUY','CASH',stock_name,fetchStockInfo(stock_name)[0],number_of_volumes)

def sellStockUtil(user_name,stock_name,number_of_volumes,stock_market_price,limit_order_bool=False):
	User_info = Userinfo.objects.get(user_name=user_name)
	user_stock_obj = User_stock.objects.filter(user_name=User_info,stock_name=stock_name)
	if not limit_order_bool:

		stock_market_price = fetchStockInfo(stock_name)[0] * float(number_of_volumes)
	print(stock_market_price)
	if user_stock_obj:
		user_stock_obj = User_stock.objects.get(user_name=User_info,stock_name=stock_name)
		user_stock_obj.user_name = User_info
		user_stock_obj.stock_name = stock_name
		user_stock_obj.number_of_volumes-= float(number_of_volumes)
		user_stock_obj.save()
	login_user_name = str(user_name) 
	login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
	bank_obj = Bank.objects.get(user_name=login_user_info_obj)   
	bank_obj.cash_available+= stock_market_price
	bank_obj.save()
	stock_obj = Stock.objects.get(stock_name=stock_name)
	stock_obj.volumes+=float(number_of_volumes)
	stock_obj.save()
	addTransaction(user_name,'SELL','CASH',stock_name,fetchStockInfo(stock_name)[0],number_of_volumes)

def fetchStockforUser(user_name,stock_name):
	#print(user_name)
	try:
		User_info = Userinfo.objects.get(user_name=user_name)
		user_stock_obj = User_stock.objects.get(user_name=User_info,stock_name=stock_name)
		stock_obj = Stock.objects.get(stock_name=stock_name)
		return [user_stock_obj.number_of_volumes,stock_obj.market_price]
	except:
		return [0,0]

def sellStockusingLO(user_name,stock_name,number_of_volumes,estimated_price,expiration_date):
	user_info = Userinfo.objects.get(user_name=user_name)
	limit_order_obj = limitOrders() 
	limit_order_obj.user_name = user_info
	limit_order_obj.stock_name = stock_name
	limit_order_obj.limitOrder_volumes = number_of_volumes
	limit_order_obj.limitOrder_price = estimated_price
	limit_order_obj.expiration_dt = expiration_date
	limit_order_obj.limitOrder_type = 'SELL'
	limit_order_obj.save()
	addTransaction(user_name,'SELL','LIMIT_ORDER',stock_name,estimated_price,number_of_volumes)

def buyStockusingLO(user_name,stock_name,number_of_volumes,estimated_price,expiration_date):
	user_info = Userinfo.objects.get(user_name=user_name)
	limit_order_obj = limitOrders() 
	limit_order_obj.user_name = user_info
	limit_order_obj.stock_name = stock_name
	limit_order_obj.limitOrder_volumes = number_of_volumes
	limit_order_obj.limitOrder_price = estimated_price
	limit_order_obj.expiration_dt = expiration_date
	limit_order_obj.limitOrder_type = 'BUY'
	limit_order_obj.save()
	addTransaction(user_name,'BUY','LIMIT_ORDER',stock_name,estimated_price,number_of_volumes)

def getLimitOrdersforUser(user_name):
	user_info = Userinfo.objects.get(user_name=user_name)
	return limitOrders.objects.filter(user_name=user_info)

def deleteLimitOrder(user_name,stock_name,expiration_dt):
	user_info = Userinfo.objects.get(user_name=user_name)
	limitOrders.objects.delete(user_name=user_info,stock_name=stock_name,expiration_dt=expiration_dt)

def deleteLimitOrderusingId(del_id):
	instance = limitOrders.objects.get(id=del_id)
	instance.delete()

def addTransaction(user_name,action,action_type,stock_name,price,volumes):
	login_user_info = Userinfo.objects.get(user_name=user_name)
	txn_obj = transactionHistory()
	txn_obj.user_name = login_user_info
	txn_obj.action = action
	txn_obj.action_type = action_type
	txn_obj.stock_name = stock_name
	txn_obj.stock_price = float(price)
	txn_obj.stock_volumes = float(volumes)
	txn_obj.total_amt = int(price) * int(volumes)
	txn_obj.txn_date = datetime.now()
	txn_obj.save()
	stock_obj = Day_trade.objects.filter(stock_name=Stock.objects.get(stock_name=stock_name),date=datetime.today())
	if stock_obj:
		stock_obj = Day_trade.objects.get(stock_name=Stock.objects.get(stock_name=stock_name),date=datetime.today())
		if txn_obj.stock_price > stock_obj.high_val:
			stock_obj.high_val = txn_obj.stock_price
		if txn_obj.stock_price < stock_obj.low_val:
			stock_obj.low_val = txn_obj.stock_price
		stock_obj.save()
	else:
		new_stock_obj = Day_trade()
		new_stock_obj.stock_name = Stock.objects.get(stock_name=stock_name)
		new_stock_obj.date = datetime.today()
		new_stock_obj.begin_val = txn_obj.stock_price
		new_stock_obj.high_val = txn_obj.stock_price
		new_stock_obj.low_val = txn_obj.stock_price
		new_stock_obj.save()
	

def fetchTransactionsforUser(user_name):
	user_info = Userinfo.objects.get(user_name=user_name)
	return transactionHistory.objects.filter(user_name=user_info)

def modifyBankAcct(user_name,amount):
	login_user_name = str(user_name) 
	login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
	bank_obj = Bank.objects.get(user_name=login_user_info_obj)
	bank_obj.cash_available+=amount
	print('Bank Affected')
	bank_obj.save() 

def checkifUserisAdmin(request):
	for g in request.user.groups.all():
		print(g.name)
		if g.name == "Stock_admin":
			return True 
	return False
	
def isMarketOpen():
	market_schedule_obj = Market.objects.get(id=1)
	now = datetime.now()

	current_time = now.time()
	print(current_time)
	if current_time>= market_schedule_obj.market_start_time and current_time <= market_schedule_obj.market_end_time:
		if market_schedule_obj.market_schedule == 'ALL_DAYS':

			return True 
		else:
			if datetime.today().weekday() <=4:
				return True 
			else:
				return False
	return False


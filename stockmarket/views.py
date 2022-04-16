from os import name
import re
from tabnanny import check
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from .utils import *


# Create your views here.

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			#UserForm(request.POST)
			if form.is_valid():
				form.save()
				# Creating the user 
				user_info_obj = Userinfo()
				
				user = form.cleaned_data.get('username')
				user_info_obj.user_name = user
				#user_info_obj.full_name = form.cleaned_data.get('first_name')
				#user_info_obj.email = form.cleaned_data.get('email')
				user_info_obj.save()
				bank_form = Bank()
				#user_info_obj = Userinfo.objects.get(name='user')
				bank_form.user_name = user_info_obj
				bank_form.cash_available = 500 
				bank_form.withdraw_date = datetime.now()
				bank_form.deposit_date = datetime.now()
				bank_form.user_deposit_limit = 500
				bank_form.user_withdrawal_limit = 500
				#bank_form_obj = BankForm(bank_form)
				bank_form.save()
				#messages.success(request, 'Account was created for ' + user)
				return redirect('home')
			

		context = {'form':form,'login_user_name':fetchUsername(request)}
		return render(request, 'stockmarket/register_user.html', context)

def login_page(request):
	#error_msg
	context = {}
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request,username=username,password=password)
			#print(username,password)
			if user is not None:
				login(request,user)
				return redirect('home')
			else:
				#messages.info(request,'Username or password is incorrect')
				error_msg = 'Username or password is incorrect'
				context = {'error_msg':error_msg,'login_user_name':fetchUsername(request)}
		return render(request,'stockmarket/login.html',context)

@login_required(login_url='login')
def home_page(request):
	if not checkifUserisAdmin(request):
		current_balance = fetchCurrentBalance(str(request.user))
		market_open = 0
		if isMarketOpen():
			market_open = 1
		else:
			market_open = 0
		
		return render(request,'stockmarket/home.html',context={'current_cash':current_balance,'stocks':fetchAllStocks(),'user_stocks':fetchstocks(request.user),'login_user_name':fetchUsername(request),'market_open':market_open})
	else:
		return render(request,'stockmarket/admin_page.html',context={'stocks':fetchAllStocks(),'login_user_name':fetchUsername(request)})

# Remove this [Jeff]
def success_page(request):
	logout(request)
	return render(request,'stockmarket/success_test.html')

# Remove this [Jeff]

def logout_page(request):
	logout(request)
	return redirect('home')

def failure_page(request):
	return render(request,'stockmarket/failure_test.html')

@never_cache
def modifyMarketSchedule(request):
	#marketScheduleForm = inlineformset_factory(fields=('market_start_time','market_end_time','market_schedule'))
	
	if request.method == 'POST':
		schedule_form = MarketForm(request.POST)
		#schedule_form.cleaned_data()
		#print(schedule_form.is_valid())
		#print(Market.objects.get(id=1))
		if schedule_form.is_valid():
			#schedule_form.save()
			market_obj = Market.objects.get(id=1
			)
			market_obj.market_start_time = schedule_form.cleaned_data['market_start_time']
			market_obj.market_end_time = schedule_form.cleaned_data['market_end_time']
			market_obj.market_schedule = schedule_form.cleaned_data['market_schedule']
			if not market_obj.market_start_time > market_obj.market_end_time:
				market_obj.save()
			#print(Market.objects.get(id=1).market_start_time)
				return redirect('home')
			else:
				schedule_form = MarketForm()
				context = {'form':schedule_form,'error_msg':'Close time should be greater than Opening Time','login_user_name':fetchUsername(request)}
				return render(request,'stockmarket/stock_admin.html',context)
		else:
			schedule_form = MarketForm()
			context = {'form':schedule_form,'error_msg':'Damn','login_user_name':fetchUsername(request)}
			return render(request,'stockmarket/stock_admin.html',context)
	else:
		#print('Function invoked')
		schedule_form = MarketForm()
		context = {'form':schedule_form,'error_msg':'','login_user_name':fetchUsername(request)}
		return render(request,'stockmarket/stock_admin.html',context)

def createStock(request):
	for stock_obj in Stock.objects.all():
		print(stock_obj.stock_created_dt)
	#print(Stock.objects.get(id=1).stock_created_dt)
	if request.method == 'POST':
		stock_form = StockForm(request.POST)
		print(stock_form.is_valid())
		if stock_form.is_valid():
			
			stock_obj = Stock()
			stock_obj.stock_name = stock_form.cleaned_data['stock_name']
			if checkifStockExists(stock_obj.stock_name):
				stock_form = StockForm()
				return render(request,'stockmarket/create_stock.html',context={'error_msg':'Stock already exists','form':stock_form,'login_user_name':fetchUsername(request)})
			stock_obj.market_price = stock_form.cleaned_data['market_price']
			stock_obj.stock_ticker = stock_form.cleaned_data['stock_ticker']
			stock_obj.volumes = stock_form.cleaned_data['volumes']
			stock_obj.status ='AVAILABLE'
			stock_obj.save()
			return redirect('home')
	else:
		stock_form = StockForm()
		context = {'form':stock_form,'login_user_name':fetchUsername(request)}
		return render(request,'stockmarket/create_stock.html',context)

def withdrawCash(request):
	if request.method == "POST":
		withdraw_amt = request.POST.get('withdraw_amt')
		login_user_name = str(request.user) 
		#print(login_user_name)
		login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
		
		#print(login_user_info_obj)
		bank_obj = Bank.objects.get(user_name=login_user_info_obj)
		current_cash = bank_obj.cash_available
		bank_obj.cash_available-=float(withdraw_amt)
		if bank_obj.cash_available < 0:
			return render(request,'stockmarket/withdrawcash.html',context={'current_cash':current_cash,'error_msg':'Cant take more than you have','login_user_name':fetchUsername(request)})
		else:
			bank_obj.save()
			return render(request,'stockmarket/cash_page.html',context={'login_user_name':fetchUsername(request)})
	else:

		login_user_name = str(request.user) 
		#print(login_user_name)
		login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
		
		#print(login_user_info_obj)
		bank_obj = Bank.objects.get(user_name=login_user_info_obj)
		
		current_cash = bank_obj.cash_available
		print(current_cash)
		return render(request,'stockmarket/withdrawcash.html',context={'current_cash':current_cash,'login_user_name':fetchUsername(request)})

def depositCash(request):
	# Can't deposit more than 1000
	# Fetch the current value 
	if request.method == "POST":
		deposit_amt = request.POST.get('deposit_amt')
		login_user_name = str(request.user) 
		#print(login_user_name)
		login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
		
		#print(login_user_info_obj)
		bank_obj = Bank.objects.get(user_name=login_user_info_obj)
		#print(type(deposit_amt))
		current_cash=bank_obj.cash_available
		bank_obj.cash_available = bank_obj.cash_available + float(deposit_amt)

		if bank_obj.cash_available > 1000:
		#print(bank_obj.cash_available)
			return render(request,'stockmarket/depositcash.html',context={'current_cash':current_cash,'error_msg':'Cant have more than 1000 in balance','login_user_name':fetchUsername(request)})
		else:
			bank_obj.save()
			current_cash=bank_obj.cash_available
			return render(request,'stockmarket/home.html',context={'current_cash':current_cash,'stocks':fetchAllStocks(),'user_stocks':fetchstocks(request.user),'login_user_name':fetchUsername(request)})
	else:
		login_user_name = str(request.user) 
		#print(login_user_name)
		login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
		
		#print(login_user_info_obj)
		bank_obj = Bank.objects.get(user_name=login_user_info_obj)
		
		current_cash = bank_obj.cash_available
		print(current_cash)
		error_msg = ''
		return render(request,'stockmarket/depositcash.html',context={'current_cash':current_cash,'error_msg':error_msg,'login_user_name':fetchUsername(request)})

def baseCash(request):
	return render(request,'stockmarket/cash_page.html',context={'login_user_name':fetchUsername(request)})

def fetchCurrentBalance(user_name):
	login_user_name = str(user_name) 
	login_user_info_obj = Userinfo.objects.get(user_name=login_user_name)
	bank_obj = Bank.objects.get(user_name=login_user_info_obj)

	return bank_obj.cash_available

def getInfo(request,stock_name):
	return JsonResponse({'data':fetchStockInfo(stock_name)})

def buyStock(request):
	if request.method == "POST":
		stock_name = request.POST.get("stocks")
		number_of_volumes =request.POST.get("number_of_vol")
		#print(stock_name)
		#print(number_of_volumes)
		#print(request.POST.get("market_value"))
		#stock_market_price = float(request.POST.get("market_value"))
		#print(stock_market_price)
		# Check if the user can buy it 
		current_balance = fetchCurrentBalance(user_name=str(request.user))
		buyStock_util(str(request.user),stock_name,number_of_volumes,stock_market_price=0,limitOrder_bool = False)
		current_balance = fetchCurrentBalance(user_name=str(request.user))
		return render(request,'stockmarket/buystock.html',context={'stocks':fetchAllStocks(),'current_cash':current_balance,'login_user_name':fetchUsername(request)})
	return render(request,'stockmarket/buystock.html',context={'current_cash':fetchCurrentBalance(str(request.user)),'stocks':fetchAllStocks(),'login_user_name':fetchUsername(request)})

def sellStock(request):
	if request.method == "POST":
		stock_name = request.POST.get("stocks")
		number_of_volumes =request.POST.get("number_of_stocks")
		sellStockUtil(str(request.user),stock_name,number_of_volumes,0,False)
		current_balance = fetchCurrentBalance(user_name=str(request.user))
		user_stocks = fetchstocks(request.user)
		return render(request,'stockmarket/sellstock.html',context={'current_cash':current_balance,'user_stocks':user_stocks,'user_name':str(request.user),'login_user_name':fetchUsername(request)})
	else:
		current_balance = fetchCurrentBalance(user_name=str(request.user))
		user_stocks = fetchstocks(request.user)
		return render(request,'stockmarket/sellstock.html',context={'current_cash':current_balance,'user_stocks':user_stocks,'user_name':str(request.user),'login_user_name':fetchUsername(request)})

def getInfoforselectedStock(request,stock_name,user_name):
	return JsonResponse({'data':fetchStockforUser(user_name,stock_name)})

def sellStock_lo(request):
	if request.method == "POST":
		current_balance = fetchCurrentBalance(user_name=str(request.user))
		user_stocks = fetchstocks(request.user)
		context_ss_lo = {'current_cash':current_balance,'user_stocks':user_stocks,'user_name':str(request.user),'login_user_name':fetchUsername(request)}
		stock_name = request.POST.get("stocks")
		number_of_volumes =request.POST.get("number_of_stocks")
		estimated_price = request.POST.get("estimated_value")
		expiration_dt = request.POST.get("sell_time")
		sellStockusingLO(str(request.user),stock_name,number_of_volumes,estimated_price,expiration_dt)
		return render(request,'stockmarket/sellstock_lo.html',context=context_ss_lo)	
	else:	
		current_balance = fetchCurrentBalance(user_name=str(request.user))
		user_stocks = fetchstocks(request.user)
		context_ss_lo = {'current_cash':current_balance,'user_stocks':user_stocks,'user_name':str(request.user),'login_user_name':fetchUsername(request)}
		return render(request,'stockmarket/sellstock_lo.html',context=context_ss_lo)

def buyStock_lo(request):
	if request.method == "POST":
		stock_name = request.POST.get("stocks")
		number_of_volumes =request.POST.get("number_of_vol")
		estimated_price = request.POST.get("estimated_value")
		expiration_dt = request.POST.get("buy_time")
		current_balance = fetchCurrentBalance(user_name=str(request.user))
		buyStockusingLO(str(request.user),stock_name,number_of_volumes,estimated_price,expiration_dt)
		return render(request,'stockmarket/buystock_lo.html',context={'stocks':fetchAllStocks(),'current_cash':current_balance,'login_user_name':fetchUsername(request)})
		
	return render(request,'stockmarket/buystock_lo.html',context={'current_cash':fetchCurrentBalance(str(request.user)),'stocks':fetchAllStocks(),'login_user_name':fetchUsername(request)})

def listLimitOrders(request,limitOrder_id):
	if request.method == "POST":
		return render(request,'stockmarket/list_limitOrder.html',context={'login_user_name':fetchUsername(request)})
	else:
		if limitOrder_id>0:
			deleteLimitOrderusingId(limitOrder_id)
		limit_order_obj_ls = getLimitOrdersforUser(str(request.user))
		lo_context = {'limitOrders':limit_order_obj_ls,'login_user_name':fetchUsername(request)}
		return render(request,'stockmarket/list_limitOrder.html',context=lo_context)

def listTransactions(request):
	if request.method == "POST":
		return render(request,'stockmarket/txnhistory.html',context={'login_user_name':fetchUsername(request)})
	else:
		txn_history = fetchTransactionsforUser(str(request.user))
		return render(request,'stockmarket/txnhistory.html',context={'transactions':txn_history,'login_user_name':fetchUsername(request)})

def fetchUsername(request):
	return str(request.user)
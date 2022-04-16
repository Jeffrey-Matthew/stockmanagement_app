## Create forms for CRUD operations 

from email.policy import default
from mimetypes import init
from time import time


from . models import Bank, Market, Stock
from django.forms import ModelForm
from django import forms
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .utils import *


class MarketForm(forms.Form,ModelForm):
	def __init__(self, *args, **kwargs):
		kwargs.update(initial={
			'market_start_time': fetchcrntMrktSchedule()[0],
			'market_end_time':fetchcrntMrktSchedule()[1],
			'market_schedule':fetchcrntMrktSchedule()[2]
		})

		super(MarketForm, self).__init__(*args, **kwargs)
		
	market_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','step':'any'}))
	market_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','step':'any'}))
	schedule_choices = (('WEEKDAYS_ONLY','WEEKDAYS_ONLY'),('ALL_DAYS','ALL_DAYS'))
	market_schedule = forms.ChoiceField(choices=schedule_choices,
		widget=forms.Select(attrs={'class':'form-select'})
	)

	class Meta:
		model = Market
		fields = ['market_schedule']

class StockForm(ModelForm):
	
	class Meta:
		model = Stock
		fields = ['stock_name','market_price','stock_ticker','volumes']
		
class CreateUserForm(UserCreationForm):    
		
	class Meta:
		model = User
		#fields = ['username','first_name','email','password1', 'password2']
		fields = ['username','password1']
		
class BankForm(ModelForm):
	class Meta:
		model = Bank
		fields = '__all__'
		
	

	

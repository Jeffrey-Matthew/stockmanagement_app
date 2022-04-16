from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(User_stock)
admin.site.register(Stock)
admin.site.register(Stock_history)
admin.site.register(Market)
admin.site.register(Day_trade)
admin.site.register(Userinfo)
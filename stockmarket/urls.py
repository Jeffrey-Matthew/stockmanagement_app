from django.urls import path,include
from . import views

urlpatterns = [
 
    path('',views.home_page,name='home'),
    path('stock_admin',views.modifyMarketSchedule,name='stock_admin'),
    path('create_stock',views.createStock,name='create_stock'),
    path('success',views.success_page,name='Success'),
    path('failure',views.failure_page,name='Failure'),
    path('register_user',views.registerPage,name='Register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('withdraw',views.withdrawCash,name='withdrawcash'),
    path('deposit',views.depositCash,name='depositcash'),
    path('cash',views.baseCash,name='cash'),
    path('get_info/<str:stock_name>/',views.getInfo,name='get_info'),
    path('buystock',views.buyStock,name='buystock'),
    path('sellstock',views.sellStock,name='sellstock'),
    path('get_selected_stock_info/<str:stock_name>/<str:user_name>',views.getInfoforselectedStock,name='getInfoforselectedStock'),
    path('sellstock_lo',views.sellStock_lo,name='sellstock_lo'),
    path('buystock_lo',views.buyStock_lo,name='buystock_lo'),
    path('limitOrders/<int:limitOrder_id>/',views.listLimitOrders,name='limitOrders'),
    path('txnHistory',views.listTransactions,name='txnHistory'),
]
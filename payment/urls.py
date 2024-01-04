
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.checkout,name='checkout'),
    path('payment/',views.payment,name="payment"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('online_place_order', views.online_place_order, name='online_place_order'),
    path('place_order/',views.place_order,name="place_order"),
    path('order_success/', views.order_success, name='order_success'),
    
]

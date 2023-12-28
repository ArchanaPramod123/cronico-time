
from django.urls import path
from .import views

urlpatterns = [
    path('user_login/',views.signin,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('',views.user_index,name='user_index'),
    path('sign_up/',views.signup,name='sign_up'),
    path('enter_otp/',views.enter_otp,name='enter_otp'),
    path('resend_otp/',views.resend_otp,name='resend_otp'),
    path('shop/', views.shop, name='shop'),
    path('search/',views.search,name='search'),
    path('shop/<slug:category_id>/', views.shop, name='products_by_category'),
    path('details/<int:category_id>/<int:product_id>', views.product_details, name='product_details'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_list, name='cart'),
    path('update-cart/', views.update_cart_item, name='update-cart'),
    path('delete-from-cart/', views.delete_cart_item, name='delete-from-cart'),
    path('user_account/', views.user_account, name='user_account'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('change_password/', views.change_password, name='change_password'),
]

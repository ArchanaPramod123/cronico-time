
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
    path('shop/<int:category_id>', views.shop, name='products_by_category'),
    path('shop/<int:brand_id>/', views.shop, name='products_by_brand'),
    path('details/<int:category_id>/<int:product_id>', views.product_details, name='product_details'),
    path('add_to_cart/',views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_list, name='cart'),
    path('update_qty',views.qty_update,name='update_qty'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    path('user_account/', views.user_account, name='user_account'),
    path('wallet/', views.wallet, name='wallet'),
    path('order_items/<int:order_number>/', views.order_items, name='order_items'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('change_password/', views.change_password, name='change_password'),
    path('cancell/<int:order_number>/',views.cancell,name='cancell'),
    path('return_order/<int:order_number>/',views.return_order,name='return_order'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:product_id>/',views.add_wishlist,name='add_wishlist'),
    path('delete_wishlist/<int:wishlist_item_id>/',views.delete_wishlist,name='delete_wishlist'),
    path('filter-product/', views.filter_product,name='filter-product'),

]

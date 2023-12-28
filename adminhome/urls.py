from django.urls import path
from .import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('admin_index/',views.admin_index,name='admin_index'),
    path('admin_category/',views.admin_category,name='admin_category'),
    path('admin_category_insert/',views.admin_category_insert,name='admin_category_insert'),
    path('admin_category_edit/<int:id>',views.admin_category_edit,name='admin_category_edit'),
    path('admin_brand/',views.admin_brand,name='admin_brand'), 
    path('admin_brand_insert/',views.admin_brand_insert,name='admin_brand_insert'),
    path('admin_brand_edit/<int:id>',views.admin_brand_edit,name='admin_brand_edit'),
    path('admin_color/',views.admin_color,name='admin_color'), 
    path('admin_color_insert/',views.admin_color_insert,name='admin_color_insert'),
    path('admin_color_edit/<int:id>',views.admin_color_edit,name='admin_color_edit'),
    path('admin_product/',views.admin_product,name='admin_product'),   
    path('admin_product_add/',views.admin_product_add,name='admin_product_add'),  
    path('admin_product_edit/<int:id>',views.admin_product_edit,name='admin_product_edit'),
    path('admin_product_delete/<int:id>',views.admin_product_delete,name='admin_product_delete'),
    path('admin_varient/',views.admin_varient,name='admin_varient'),  
    path('admin_varient_add/',views.admin_varient_add,name='admin_varient_add'), 
    path('admin_varient_edit/<int:id>',views.admin_varient_edit,name='admin_varient_edit'), 
    path('admin_varient_delete/<int:id>',views.admin_varient_delete,name='admin_varient_delete'), 
    path('order/',views.order,name='order'),
    path('orderitems/',views.orderitems,name='orderitems'),
    path('customers/',views.customers,name='customers'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
]

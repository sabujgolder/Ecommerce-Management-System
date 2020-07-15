from django.contrib import admin
from django.urls import path
from ecmsapp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),

    path('login',views.login_view,name='login'),
    path('register',views.registerPage,name='register'),
    path('logout',views.logoutUser,name='logout'),


    path('chart',views.data_chart,name='data_chart'),


    path('shop_owners_forum/',views.shop_owners_forum,name='shop_owners_forum'),
    path('shop_owner_data/<str:pk>/',views.shop_owner_data,name='shop_owner_data'),
    path('shop_owner/<str:pk>/',views.shop_owner,name='shop_owner'),
    path('shop/<str:pk>/',views.shop,name='shop'),
    path('all_shops/',views.all_shops,name='all_shops'),

    path('add_product/<str:pk>/',views.add_products,name='add_product'),
    path('products/<str:pk>/',views.products,name='products'),
    path('update_product/<str:pk>/',views.update_product,name='update_product'),
    path('bulk_product_update/<str:pk>/',views.bulk_product_update,name='bulk_product_update'),
    path('delete_product/<str:pk>/',views.delete_product,name='delete_product'),


    path('customer_forum/',views.customer_forum,name='customer_forum'),
    path('customer/<str:pk>/',views.customer,name='customer'),
    path('customers/',views.customers,name='customers'),
    path('create_order/<str:pk>/',views.create_order,name='create_order'),
    path('update_customer/<str:pk>/',views.Update_Customer,name='update_customer'),

    path('update_order/<str:pk>/',views.Update_Order,name='update_order'),
    path('delete_order/<str:pk>/',views.Delete_Order,name='delete_order'),

    path('post_details/<str:pk>/',views.customer_post_detail,name='post_detail'),
    path('shop_owner_post_detail/<str:pk>/',views.shop_owner_post_detail,name='shop_owner_post_detail'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

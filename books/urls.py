
from django.urls import path,include
from . import views#from the same folder import views file
urlpatterns =[
    path('',views.index,name="home"),
    path('login',views.loginUser,name="login"),
    path('signup',views.signup,name="signup"),
    path('details<int:id>',views.product_details,name="product_details"),
    path('cart/', views.cart_view,name="cart"),
    path('orders', views.orders_view,name="orders"),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('shipping_cart/', views.shipping_details_cart, name='shipping_details_cart'),
    path('logout/', views.logout_view, name='logout'),
]


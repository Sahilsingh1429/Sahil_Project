from django.contrib import admin
from django.urls import path
from shoppingapp.views import *
urlpatterns = [
    path('',index,name='index'),
    path('contact/',contact,name='contact'),
    path('faqs/',faqs,name='faqs'),
    path('about/',about,name='about'),
    path('help/',help,name='help'),
    path('icons/',icons,name='icons'),
    # path('payment/',payment,name='payment'),
    path('privacy/',privacy,name='privacy'),
    path('product/',product,name='product'),
    path('product2/',product2,name='product2'),
    path('single/',single,name='single'),
    path('single2/',single2,name='single2'),
    path('terms/',terms,name='terms'),
    path('typography/',typography,name='typography'),
    path('checkout/',checkout,name='checkout'),
    path('register/',register,name='register'),
     path('login/',login,name='login'),
     path('otp/',otp,name='otp'),
    path('logout/',logout,name='logout'),
    path('add_to_cart/<int:pid>',add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('del_cart_row/<int:cid>',del_cart_row,name='del_cart_row'),
    path('start_payment/',homepage,name='start_payment'),
    path('start_payment/paymenthandler/',paymenthandler, name='paymenthandler')
]
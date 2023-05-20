from django.urls import path
from .views import *

urlpatterns = [
    path('seller_register/',seller_register,name = 'seller_register'),
    path('seller_login/',seller_login,name = 'seller_login'),
    path('',seller_index,name='seller_index'),
    path('seller_profile/',seller_profile,name='seller_profile'),
    path('add_product/',add_product,name='add_product'),
    path('seller_logout/',seller_logout,name='seller_logout')
] 
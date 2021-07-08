from django.urls import path
from .views import *

urlpatterns = [
    path('create',create_new_transaction),
    path('add_inventory',add_multiple_inventory_items),
    path('delete',delete_transaction),
    path('get_details',get_transaction_details),
]

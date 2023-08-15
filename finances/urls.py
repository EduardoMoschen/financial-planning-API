from django.urls import path
from finances.views import accounts_list, account_detail

urlpatterns = [
    path('accounts/', accounts_list, name='account_list'),
    path('account/<int:pk>', account_detail, name='account_detail')
]

from django.urls import path
from finances import views

urlpatterns = [
    path(
        'api/accounts/',
        views.AccountAPIList.as_view(),
        name='accounts_list'
    ),
    path(
        'api/account/<int:pk>/',
        views.AccountAPIDetail.as_view(),
        name='account_detail'
    ),
    path(
        'api/owners/',
        views.OwnerAPIList.as_view(),
        name='owners_list'
    ),
    path(
        'api/owner/<int:pk>/',
        views.OnwerAPIDetail.as_view(),
        name='owner_detail'
    ),
    path(
        'api/categories/',
        views.CategoryAPIList.as_view(),
        name='categories_list'
    ),
    path(
        'api/category/<int:pk>/',
        views.CategoryAPIDetail.as_view(),
        name='category_detail'
    ),
    path(
        'api/transactions/',
        views.TransactionAPIList.as_view(),
        name='transactions_list'
    )
]

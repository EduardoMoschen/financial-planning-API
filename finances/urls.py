from django.urls import path
from finances import views

urlpatterns = [
    path(
        'api/accounts/',
        views.AccountAPIList.as_view(),
        name='account_list'
    ),
    path(
        'api/account/<int:pk>',
        views.AccountAPIDetail.as_view(),
        name='account_detail'
    )
]

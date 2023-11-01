from django.urls import path
from finances import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# Define os endpoints e suas respectivas views para a API.
urlpatterns = [
    # Endpoint para listar todas as contas cadastradas.
    path(
        'api/accounts/',
        views.AccountAPIList.as_view(),
        name='accounts_list'
    ),

    # Endpoint para detalhar uma conta financeira específica com base na 'pk'.
    path(
        'api/account/<int:pk>/',
        views.AccountAPIDetail.as_view(),
        name='account_detail'
    ),

    # Endpoint para listar todos os titulares de contas financeiras.
    path(
        'api/owners/',
        views.OwnerAPIList.as_view(),
        name='owners_list'
    ),

    # Endpoint para detalhar um titular específico com base na 'pk'.
    path(
        'api/owner/<int:pk>/',
        views.OnwerAPIDetail.as_view(),
        name='owner_detail'
    ),

    # Endpoint para listar todas as categorias de despesas.
    path(
        'api/categories/',
        views.CategoryAPIList.as_view(),
        name='categories_list'
    ),

    # Endpoint para detalhar uma categoria específica com base na 'pk'.
    path(
        'api/category/<int:pk>/',
        views.CategoryAPIDetail.as_view(),
        name='category_detail'
    ),

    # Endpoint para listar todas as transações financeiras.
    path(
        'api/transactions/',
        views.TransactionAPIList.as_view(),
        name='transactions_list'
    ),

    # Endpoint para detalhar uma transação específica com base na 'pk'.
    path(
        'api/transaction/<int:pk>/',
        views.TransactionAPIDetail.as_view(),
        name='transaction_detail'
    ),

    # Endpoint para listar todos os orçamentos financeiros.
    path(
        'api/budgets/',
        views.BudgetAPIList.as_view(),
        name='budgets_list'
    ),

    # Endpoint para detalhar um orçamento específico com base na 'pk'.
    path(
        'api/budget/<int:pk>/',
        views.BudgetAPIDetail.as_view(),
        name='budget_detail'
    ),

    # Endpoint para obter o token de acesso (login).
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    # Endpoint para atualizar o token de acesso.
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # Endpoint para verificar a validade do token de acesso.
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]

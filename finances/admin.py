from django.contrib import admin
from finances.models import Account, Category, Transaction, Budget


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    ...


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    ...

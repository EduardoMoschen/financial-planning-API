from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """
    Representação da conta financeira do usuário.

    Atributos:
        owner: O usuário associado a esta conta.
        name: O tipo de conta. Por exemplo, Conta Corrente.
        balance: O valor monetário atual disponível na conta.
        created_at: A data e hora da criação.

    Métodos:
        __str__: Retorna uma representação em string da conta.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=65)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Representação da transação financeira associada a uma conta.

    Atributos:
        account: A transação pertence a uma conta específica.
        amount: O valor monetário da transação.
        description: Uma descrição opcional da transação, feita pelo usuário.
        timestamp: O timestamp da criação da transação.

    Métodos:
        __str__: Retorna uma representação em string da transação.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount} - {self.description}'


class Category(models.Model):
    """
    Representação da categoria da transação.

    Atributos:
        name: O nome da categoria. Por exemplo, Alimentação.

    Métodos:
        __str__: Retorna uma representação em string da categoria.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Budget(models.Model):
    """
    Representação do orçamento associado a uma categoria.

    Atributos:
        category: A categoria a qual o orçamento pertence.
        amount: O valor monetário do orçamento.
        start_date: A data de início do período do orçamento.
        end_date: A data de término do período do orçamento.

    Métodos:
        __str__: Retorna uma representação em string do orçamento.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.category.name} - {self.amount}'
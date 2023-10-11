from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Account(models.Model):
    """
    Representação da conta financeira do usuário.

    Atributos:
        owner: O usuário associado a esta conta.
        name: O tipo de conta. Por exemplo, Conta Corrente.
        balance: O valor monetário atual disponível na conta.
        created_at: A data e hora da criação da conta.

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
        return f'Account of {self.owner.first_name} {self.owner.last_name} - '\
            f'{self.name}'


class Category(models.Model):
    """
    Representação da categoria da transação.

    Atributos:
        name: O nome da categoria. Por exemplo, "Alimentação".

    Métodos:
        __str__: Retorna uma representação em string da categoria.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Category: {self.name}'


class Transaction(models.Model):
    """
    Representação da transação financeira associada a uma conta.

    Atributos:
        account: A conta à qual a transação pertence.
        category: A categoria da transação.
        amount: O valor monetário da transação.
        description: Uma descrição opcional da transação, feita pelo usuário.
        timestamp: O timestamp da criação da transação.

    Métodos:
        __str__: Retorna uma representação em string da transação.
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'Value: {self.amount} - Description: {self.description}'


class Budget(models.Model):
    """
    Representação do orçamento associado a uma categoria.

    Atributos:
        account: A conta à qual o orçamento pertence.
        category: A categoria à qual o orçamento pertence.
        amount: O valor monetário do orçamento.
        start_date: A data de início do período do orçamento.
        end_date: A data de término do período do orçamento.
        spent: O valor gasto dentro do período de orçamento.

    Métodos:
        __str__: Retorna uma representação em string do orçamento.
        update_spent: Atualiza o valor gasto com base nas transações dentro do
        período do orçamento.
    """

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Budget to {self.category.name} - {self.amount}'

    def update_spent(self, transaction_amount):
        """
        Atualiza o valor gasto com base nas transações dentro do período do
        orçamento.
        """

        spent_amount = Transaction.objects.filter(
            category=self.category,
            date__range=(self.start_date, self.end_date)
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        self.spent = spent_amount + transaction_amount
        self.save()

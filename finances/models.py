from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """
    Model que representa a conta financeira do usuário.

    Atributos:
        owner: O proprietário da conta.
        name: O tipo de conta. Por exemplo, Conta Corrente.
        balance: O saldo atual da conta.
        created_at: A data e hora da criação.
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

from django.test import TestCase
from finances.models import Account, Category, Transaction, Budget
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class BudgetModelTestCase(TestCase):
    """
    Testes para o modelo Budget.

    Esta classe contém testes para o modelo Budget, que representa um orçamento
    financeiro.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria as instâncias
        iniciais de objetos necessárias para os testes.
        """

        self.user = User.objects.create_user(
            username="user1",
            password="password1",
            first_name="Carlos",
            last_name="Alberto",
            email="carlos@email.com"
        )

        self.account = Account.objects.create(
            owner=self.user,
            name="Current Account",
            balance=10000
        )

        self.category = Category.objects.create(name="Food")

        self.start_date = timezone.make_aware(datetime(2023, 1, 1))
        self.end_date = timezone.make_aware(datetime(2023, 1, 31))

        self.budget = Budget.objects.create(
            account=self.account,
            category=self.category,
            amount=1000,
            start_date=self.start_date,
            end_date=self.end_date,
            spent=0,
        )

        self.transaction = Transaction.objects.create(
            account=self.account,
            category=self.category,
            amount=250.00,
            date=timezone.make_aware(datetime(2023, 1, 15)),
            description='Shopping at the supermarket',
        )

    def test_budget_str_with_expected_output(self):
        """
        Testa o método __str__() do modelo Budget.

        Este teste verifica se o método __str__() do modelo Budget retorna a
        saída esperada, que inclui o nome da categoria e o valor do orçamento.
        """

        expected_output = f'Budget to {self.budget.category.name} - ' \
                          f'{self.budget.amount}'
        self.assertEqual(str(self.budget), expected_output)

    def test_update_spent(self):
        """
        Testa o método update_spent() do modelo Budget.

        Este teste verifica se o método update_spent() do modelo Budget
        atualiza corretamente o valor gasto com base em uma transação.
        """

        self.budget.update_spent(self.transaction.amount)
        updated_budget = Budget.objects.get(pk=self.budget.pk)
        self.assertEqual(updated_budget.spent, 250)

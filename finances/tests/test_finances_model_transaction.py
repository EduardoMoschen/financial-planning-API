from django.test import TestCase
from finances.models import Transaction, Account, Category
from django.contrib.auth.models import User


class TransactionModelTestCase(TestCase):
    """
    Teste para o modelo Transaction.

    Esta classe contém teste para o modelo Transaction, que representa uma
    transação financeira.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria as instâncias
        iniciais de objetos necessárias para os testes.
        """

        self.user = User.objects.create_user(
            username='user1',
            password='password1',
            first_name='Carlos',
            last_name='Alberto',
            email='carlos@email.com'
        )

        self.account = Account.objects.create(
            owner=self.user,
            name='Current Account',
            balance=10000
        )

        self.category = Category.objects.create(name='Food')

        self.transaction = Transaction.objects.create(
            account=self.account,
            category=self.category,
            amount=250,
            description='Shopping at the supermarket for the weekend'
        )

    def test_transaction_str_with_expected_output(self):
        """
        Testa o método __str__() do modelo Transaction.

        Este teste verifica se o método __str__() do modelo Transaction retorna
        a saída esperada, que inclui o valor e a descrição da transação.
        """

        expected_output = f'Value: {self.transaction.amount} - ' \
                          f'Description: {self.transaction.description}'
        self.assertEqual(str(self.transaction), expected_output)

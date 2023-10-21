from django.test import TestCase
from django.contrib.auth.models import User
from finances.models import Account


class AccountModelTestCase(TestCase):
    """
    Teste para o modelo Account.

    Esta classe contém testes para o modelo Account, que representa uma conta
    financeira.
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

    def test_account_str_with_expected_output(self):
        """
        Testa o método __str__() do modelo Account.

        Este teste verifica se o método __str__() do modelo Account retorna a
        saída esperada, que inclui o primeiro e último nome do titular, e o
        tipo de conta financeira.
        """

        expected_output = f'Account of {self.user.first_name} ' \
            f'{self.user.last_name} - {self.account.name}'
        self.assertEqual(str(self.account), expected_output)

from django.test import TestCase
from django.contrib.auth.models import User
from finances.models import Account


class AccountModelTestCase(TestCase):
    """
    Teste para o modelo Account.

    Esta classe ccontém teste para o modelo Account, que representa uma conta
    financeira.
    """

    def test_account_str_with_expected_output(self):
        """
        Testa o método __str__() do modelo Account.

        Este teste verifica se o método __str__() do modelo Account retorna a
        saída esperada, que inclui o primeiro e último nome do titular, e o
        tipo de conta financeira.

        Casos de Teste:
            - Cria um usuário e uma conta financeira.
            - Compara a representação da string da conta financeira com a saóda
            esperada.

        Notas:
            - Deve se certificar de ter criado instâncias de objetos
            relacionados para garantir a integridade do teste.
        """

        user = User.objects.create(
            username="user1",
            password="password1",
            first_name="Carlos",
            last_name="Alberto",
            email="carlos@email.com"
        )

        account = Account.objects.create(
            owner=user,
            name="Current Account",
            balance=10000
        )

        expected_output = f'Account of {user.first_name} {user.last_name} - '\
            f'{account.name}'
        self.assertEqual(str(account), expected_output)

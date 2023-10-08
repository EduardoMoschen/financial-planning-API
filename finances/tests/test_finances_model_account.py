from django.test import TestCase
from django.contrib.auth.models import User
from finances.models import Account


class AccountModelTestCase(TestCase):
    """
    Testes para a classe Account do modelo.

    Este conjunto de testes verifica o comportamento do método __str__ da
    classe Account em diferentes cenários.
    """

    def test_account_str_with_expected_output(self):
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

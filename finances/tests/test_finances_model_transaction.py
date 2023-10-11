from django.test import TestCase
from finances.models import Transaction, Account, Category
from django.contrib.auth.models import User


class TransactionModelTestCase(TestCase):
    """
    Teste para o modelo Transaction.

    Esta classe contém teste para o modelo Transaction, que representa uma
    transação financeira.
    """

    def test_transaction_str_with_expected_output(self):
        """
        Testa o método __str__() do modelo Transaction.

        Este teste verifica se o método __str__() do modelo Transaction retorna
        a saída esperada, que inclui o valor e a descrição da transação.

        Casos de Teste:
            - Cria um usuário, uma conta, uma categoria e uma transação.
            - Compara a representação da string da transação com a saída
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

        category = Category.objects.create(name="Food")

        transaction = Transaction.objects.create(
            account=account,
            category=category,
            amount=250,
            description='Shopping at the supermarket for the weekend'
        )

        expected_output = f'Value: {transaction.amount} - '\
            f'Description: {transaction.description}'

        self.assertEqual(str(transaction), expected_output)

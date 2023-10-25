from django.test import TestCase
from django.contrib.auth.models import User
from finances.models import Account
from finances.serializers import AccountSerializer
from rest_framework.exceptions import ValidationError


class AccountSerializerTestCase(TestCase):
    """
    Testes para o serializador de conta.

    Esta classe contém testes para o serializador de Account, que é responsável
    por validar e transformar dados
    de contas financeiras em um formato adequado para o uso na API.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria instâncias
        iniciais de objetos necessários para os testes.
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
            name='Conta Corrente',
            balance=1000
        )

    def test_valid_account(self):
        """
        Testa a validação de uma conta válida.

        Este teste verifica se o serializador aceita corretamente uma conta
        válida e retorna os dados esperados.
        """

        serializer = AccountSerializer(instance=self.account)
        data = serializer.data
        self.assertEqual(data['owner'], self.user.id)
        self.assertEqual(data['name'], 'Conta Corrente')
        self.assertEqual(float(data['balance']), 1000)

    def test_invalid_negative_balance(self):
        """
        Testa a validação de um saldo negativo.

        Este teste verifica se o serializador rejeita corretamente um saldo
        negativo e retorna uma mensagem de erro apropriada.
        """

        invalid_data = {
            'owner': self.user.id,
            'name': 'Conta Poupança',
            'balance': -100
        }

        serializer = AccountSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            context.exception.detail,
            {'balance': ['The balance must not be negative.']}
        )

    def test_invalid_missing_owner(self):
        """
        Testa a validação de proprietário ausente.

        Este teste verifica se o serializador rejeita corretamente uma conta
        sem proprietário e retorna uma mensagem de erro apropriada.
        """

        invalid_data = {
            'name': 'Conta Investimento',
            'balance': 2000
        }

        serializer = AccountSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
                         'owner': ['Este campo é obrigatório.']})

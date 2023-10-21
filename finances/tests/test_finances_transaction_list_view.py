from django.test import TestCase
from finances.models import Transaction, Account, Category, Budget
from finances.serializers import TransactionSerializer
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class TransactionAPIListTest(TestCase):
    """
    Testes para a API de TransactionAPIList.

    Esta classe contém testes para os métodos da API de TransactionAPIList, que
    lida com operações relacionadas às transações.
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
            name='Current Account 1',
            balance=10000
        )

        self.category_1 = Category.objects.create(
            name='Academia'
        )

        self.category_2 = Category.objects.create(
            name="Medicamentos"
        )

        self.transaction_1 = Transaction.objects.create(
            amount=150,
            description='Compra de remédios na farmácia.',
            account=self.account,
            category=self.category_1
        )

        self.budget = Budget.objects.create(
            start_date='2023-08-01',
            end_date='2023-08-31',
            amount=150,
            account=self.account,
            category=self.category_2
        )

        self.client = APIClient()

    def test_get_transactions(self):
        """
        Testa o método GET para obter todas as transações cadastradas.

        Este teste verifica se o método GET retorna todas as transações com o
        status HTTP 200 OK.
        """

        response = self.client.get('/api/transactions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_no_transactions(self):
        """
        Testa o método GET quando não há transações cadastradas.

        Este teste verifica se o método GET retorna a mensagem apropriada
        quando não há transações cadastradas.
        """

        Transaction.objects.all().delete()

        response = self.client.get('/api/transactions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'message': 'There are no registered transactions.'}
        )

    def test_create_transaction(self):
        """
        Testa o método POST para criar uma nova transação.

        Este teste verifica se o método POST cria uma nova transação
        corretamente e retorna o status HTTP 201 CREATED.
        """

        new_transaction_data = {
            'amount': 50,
            'description': 'Compra de protetor solar.',
            'account': self.account.id,
            'category': self.category_2.id,
        }

        response = self.client.post(
            '/api/transactions/',
            data=new_transaction_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cretaed_transaction = Transaction.objects.get(category=self.category_2)
        self.assertEqual(cretaed_transaction.category.id, self.category_2.id)

        serializer = TransactionSerializer(cretaed_transaction)
        self.assertEqual(response.data, serializer.data)

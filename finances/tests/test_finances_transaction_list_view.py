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

        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
        )

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

        self.client_admin = APIClient()
        self.client_admin.force_authenticate(
            user=self.admin)  # Authenticate as admin

        self.client_user = APIClient()
        self.client_user.force_authenticate(
            user=self.user)  # Authenticate as user

    def test_get_transactions(self):
        """
        Testa se apenas o administrador pode obter todas as transações.

        Verifica se o método GET retorna todas as transações com o
        status HTTP 200 OK para o administrador e status HTTP 403 FORBIDDEN
        para o usuário comum.
        """

        response_admin = self.client_admin.get('/api/transactions/')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_admin['content-type'], 'application/json')

        response_user = self.client_user.get('/api/transactions/')
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_transactions(self):
        """
        Testa se a mensagem apropriada é retornada quando não há transações.

        Verifica se o método GET retorna a mensagem apropriada quando não há
        transações cadastradas.
        """

        Transaction.objects.all().delete()
        response = self.client_admin.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'message': 'There are no registered transactions.'}
        )

    def test_create_transaction(self):
        """
        Testa se tanto o usuário autenticado quanto o administrador podem criar
        uma nova transação.

        Verifica se o método POST cria uma nova transação corretamente e
        retorna o status HTTP 201 CREATED para ambos, o usuário autenticado e o
        administrador.
        """

        new_transaction_data = {
            'amount': 50,
            'description': 'Compra de protetor solar.',
            'account': self.account.id,
            'category': self.category_2.id,
        }

        response_user = self.client_user.post(
            '/api/transactions/',
            data=new_transaction_data,
            format='json'
        )
        self.assertEqual(response_user.status_code, status.HTTP_201_CREATED)

        created_transaction_user = Transaction.objects.get(
            description='Compra de protetor solar.',
            amount=50
        )
        serializer_user = TransactionSerializer(created_transaction_user)
        self.assertEqual(response_user.data, serializer_user.data)

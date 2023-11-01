from rest_framework.test import APITestCase
from finances.models import Account
from finances.serializers import AccountSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class AccountAPIListTest(APITestCase):
    """
    Testes para a API de Account.

    Esta classe contém testes para os métodos da API de Account, que lida com
    operações relacionadas a contas financeiras dos usuários.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria instâncias
        iniciais de objetos necessários para os testes.
        """

        self.admin = User.objects.create_user(
            username='admin',
            password='admin_password',
            is_staff=True
        )

        self.user = User.objects.create_user(
            username='user1',
            password='password1',
            first_name='Carlos',
            last_name='Alberto',
            email='carlos@email.com'
        )

        self.account_1 = Account.objects.create(
            owner=self.user,
            name='Current Account 1',
            balance=10000
        )

        self.account_2 = Account.objects.create(
            owner=self.user,
            name='Current Account 2',
            balance=10000
        )

        self.client = APIClient()

    def test_get_accounts(self):
        """
        Testa o método GET para obter todas as contas.

        Este teste verifica se o método GET retorna todas as contas com o
        status HTTP 200 OK.
        """

        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_no_accounts(self):
        """
        Testa o método GET quando não há contas.

        Este teste verifica se o método GET retorna a mensagem apropriada
        quando não há contas registradas.
        """

        self.client.force_authenticate(user=self.admin)
        Account.objects.all().delete()
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'message': 'There are no registered accounts.'}
        )

    def test_create_owner(self):
        """
        Testa o método POST para criar uma nova conta.

        Este teste verifica se o método POST cria uma nova conta corretamente e
        retorna o status HTTP 201 CREATED.
        """

        self.client.force_authenticate(user=self.user)
        new_account_data = {
            'name': 'Savings Account',
            'balance': 5000,
            'owner': self.user.id
        }

        response = self.client.post(
            '/api/accounts/',
            data=new_account_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_account = Account.objects.get(name=new_account_data['name'])
        self.assertEqual(created_account.name, new_account_data['name'])
        self.assertEqual(created_account.balance, new_account_data['balance'])
        self.assertEqual(created_account.owner.id, self.user.id)

        serializer = AccountSerializer(created_account)
        self.assertEqual(response.data, serializer.data)

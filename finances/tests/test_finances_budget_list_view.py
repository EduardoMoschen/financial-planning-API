from rest_framework.test import APITestCase
from finances.models import Category, Account, Transaction, Budget
from finances.serializers import BudgetSerializer
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class BudgetAPIListTest(APITestCase):
    """
    Teste para a API de BudgetAPIList.

    Esta classe contém testes para os métodos da API de BudgetAPIList, que lida
    com operações relacionadas aos orçamentos das contas bancárias.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria instâncias
        iniciais de objetos necessários para os testes.
        """

        self.user = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@admin.com'
        )

        self.account = Account.objects.create(
            owner=self.user,
            name='Conta Corrente',
            balance=1000
        )

        self.category_1 = Category.objects.create(
            name='Academia'
        )

        self.category_2 = Category.objects.create(
            name='Supermercado'
        )

        self.transaction = Transaction.objects.create(
            amount=200,
            description='Pagamento de academia',
            account=self.account,
            category=self.category_1
        )

        self.budget_1 = Budget.objects.create(
            start_date='2023-08-01',
            end_date='2023-08-31',
            amount=150,
            account=self.account,
            category=self.category_1
        )

        self.budget_2 = Budget.objects.create(
            start_date='2023-09-01',
            end_date='2023-09-30',
            amount=150,
            account=self.account,
            category=self.category_1
        )

        self.client = APIClient()

    def test_get_budgets(self):
        """
        Testa o método GET para obter todos os orçamentos cadastrados.

        Este teste verifica se o método GET retorna todos os orçamentos com
        status HTTP 200 OK.
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        budgets = Budget.objects.all()
        serializer = BudgetSerializer(budgets, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_no_budgets(self):
        """
        Testa o método GET quando não há orçamentos cadastrados.

        Este teste verifica se o método GET retorna a mensagem apropriada
        quando não há orçamentos cadastrados.
        """

        self.client.force_authenticate(user=self.user)

        Budget.objects.all().delete()

        response = self.client.get('/api/budgets/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': 'There are no registered budgets.'})

    def test_create_budget(self):
        """
        Testa o método POST para criar um novo orçamento.

        Este teste verifica se o método POST cria um novo orçamento
        corretamente e retorna o status HTTP 201 CREATED.
        """

        self.client.force_authenticate(user=self.user)

        new_budget_data = {
            "account": self.account.id,
            "category": self.category_2.id,
            "amount": "500.00",
            'start_date': '2023-09-01',
            'end_date': '2023-09-30'
        }

        response = self.client.post(
            '/api/budgets/',
            data=new_budget_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_budget = Budget.objects.get(category=self.category_2)
        self.assertEqual(created_budget.category.id, self.category_2.id)

        serializer = BudgetSerializer(created_budget)
        self.assertEqual(response.data, serializer.data)

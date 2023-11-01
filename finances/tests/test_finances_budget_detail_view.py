from django.test import TestCase, RequestFactory
from finances.models import Category, Account, Transaction, Budget
from finances.views import BudgetAPIDetail
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
import json
from datetime import datetime


class BudgetAPIDetailTest(TestCase):
    """
    Teste para a classe BudgetAPIDetail.

    Esta classe contém testes para os métodos da classe BudgetAPIDetail, que
    lida com operações detalhadas relacionadas a um orçamento específico.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria instâncias
        iniciais de objetos necessários para os testes.
        """

        self.factory = RequestFactory()

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
            category=self.category_1,
            date=datetime.strptime('2023-08-15', '%Y-%m-%d')
        )

        start_date_1 = datetime.strptime('2023-08-01', '%Y-%m-%d')
        end_date_1 = datetime.strptime('2023-08-31', '%Y-%m-%d')

        self.budget_1 = Budget.objects.create(
            start_date=start_date_1,
            end_date=end_date_1,
            amount=150,
            account=self.account,
            category=self.category_1,
            spent=0
        )

        start_date_2 = datetime.strptime('2023-09-01', '%Y-%m-%d')
        end_date_2 = datetime.strptime('2023-09-30', '%Y-%m-%d')

        self.budget_2 = Budget.objects.create(
            start_date=start_date_2,
            end_date=end_date_2,
            amount=150,
            account=self.account,
            category=self.category_1,
            spent=0
        )

    def test_get(self):
        """
        Testa o método GET para obter o orçamento específico.

        Este teste verifica se o método GET retorna o status HTTP 200 OK para
        uma solicitação de listagem com detalhes de um orçamento válido.
        """

        view = BudgetAPIDetail.as_view()
        request = self.factory.get(f'/api/budget/{self.budget_1.pk}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.budget_1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_method_success(self):
        """
        Testa o método PUT para atualização dos dados do orçamento.

        Este teste verifica se o método PUT retorna o status HTTP 200 OK para
        uma solicitação de atualização com os dados válidos do orçamento.
        """

        view = BudgetAPIDetail.as_view()
        data = {
            'account': self.account.id,
            'category': self.category_1.id,
            'amount': 200,
            'start_date': '2023-08-01',
            'end_date': '2023-08-31',
            'spent': 0
        }
        request = self.factory.put(
            f'/api/budget/{self.budget_1.pk}/',
            data=json.dumps(data),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.budget_1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Budget.objects.get(pk=self.budget_1.pk).amount, 200)

    def test_put_method_validation_error(self):
        """
        Testa o método PUT para atualização dos dados inválidos do orçamento.

        Este teste verifica se o método PUT retorna o status HTTP 400 BAD
        REQUEST para uma solicitação de atualização com os dados inválidos do
        orçamento.
        """

        view = BudgetAPIDetail.as_view()
        data = {
            'account': self.account.id,
            'category': self.category_1.id,
            'amount': -200,  # Valor inválido para amount
            'start_date': '2023-08-01',
            'end_date': '2023-08-31',
            'spent': 0
        }
        request = self.factory.put(
            f'/api/budget/{self.budget_1.pk}/',
            data=json.dumps(data),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.budget_1.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_delete(self):
        """
        Testa o método DELETE para excluir os dados do orçamento específico.

        Este teste verifica se o método DELETE retorna o status HTTP 204 NO
        CONTENT para uma solicitação de exclusão válida do orçamento.
        """

        view = BudgetAPIDetail.as_view()
        request = self.factory.delete(f'/api/budget/{self.budget_1.pk}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.budget_1.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

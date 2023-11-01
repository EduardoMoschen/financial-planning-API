from django.test import TestCase
from finances.views import CategoryAPIDetail
from finances.models import Category, Account, Transaction, Budget
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APIRequestFactory


class CategoryAPIDetailTest(TestCase):
    """
    Teste para a classe CategoryAPIDetail.

    Esta classe contém testes para os métodos da classe CategoryAPIDetail, que
    lida com operações detalhadas relacionadas a uma categoria específica.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria uma instância
        inicial de objetos necessários para os testes.
        """

        # self.factory = RequestFactory()

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

        self.category = Category.objects.create(
            name='Academia'
        )

        self.transaction = Transaction.objects.create(
            amount=200,
            description='Pagamento de academia',
            account=self.account,
            category=self.category
        )

        self.budget = Budget.objects.create(
            start_date='2023-08-01',
            end_date='2023-08-31',
            amount=150,
            account=self.account,
            category=self.category
        )

        self.admin = User.objects.create_user(
            username='admin',
            password='admin_password',
            is_staff=True
        )

        self.factory = APIRequestFactory()

    def test_get(self):
        """
        Testa o método GET para obter uma categoria específica.

        Este teste verifica se o método GET retorna o status HTTP 200 OK para
        uma solicitação de listagem com detalhes de uma categoria válida.
        """

        view = CategoryAPIDetail.as_view()
        request = self.factory.get(f'/api/category/{self.category.pk}/')
        force_authenticate(request, user=self.admin)
        response = view(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        """
        Testa o método PUT para atualizar os dados de uma categoria específica.

        Este teste verifica se o método PUT retorna o status HTTP 200 OK para
        uma solicitação de atualização com os dados válidos da categoria.
        """

        view = CategoryAPIDetail.as_view()

        new_data_category = {'name': 'Medicamentos'}

        request = self.factory.put(
            f'/api/category/{self.category.pk}/',
            data=new_data_category,
            format='json'
        )

        force_authenticate(request, user=self.admin)
        response = view(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Testa o método DELETE para exclusão de uma categoria específica.

        Este teste verifica se o método DELETE retorna o status HTTP 204 NO
        CONTENT para uma solicitação de exclusão válida.
        """

        view = CategoryAPIDetail.as_view()
        request = self.factory.delete(f'/api/category/{self.category.pk}/')
        force_authenticate(request, user=self.admin)
        response = view(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(
            category=self.category).exists()
        )
        self.assertFalse(Budget.objects.filter(
            category=self.category).exists()
        )

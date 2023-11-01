from rest_framework.test import APITestCase
from finances.models import Account
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class AccountAPIDetailTest(APITestCase):
    """
    Testes para a classe AccountAPIDetail.

    Esta classe contém testes para os métodos da classe AccountAPIDetail, que
    lida com operações detalhadas relacionadas a uma conta financeira
    específica do usuário.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria uma instância
        inicial de objeto Account necessária para os testes.
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
            balance=100.00
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Authenticate as user

    def test_get(self):
        """
        Testa o método GET para obter a conta específica.

        Este teste verifica se o método GET retorna o status HTTP 200 OK para
        uma solicitação de listagem com detalhes de uma conta válida.
        """

        response = self.client.get(f'/api/account/{self.account.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        """
        Testa o método PATCH para atualizar os dados de uma conta específica.

        Este teste verifica se o método PATCH retorna o status HTTP 200 OK para
        uma solicitação de atualização de conta válida.
        """

        data = {
            'name': 'Conta Poupança',
            'balance': 200.00
        }

        response = self.client.patch(
            f'/api/account/{self.account.pk}/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Testa o método DELETE para exclusão de uma conta específica.

        Este teste verifica se o método DELETE retorna o status HTTP 204 No
        Content para uma solicitação de exclusão de conta válida.
        """

        response = self.client.delete(f'/api/account/{self.account.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

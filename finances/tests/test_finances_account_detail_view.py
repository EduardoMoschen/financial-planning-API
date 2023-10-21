from django.test import TestCase, RequestFactory
from finances.views import AccountAPIDetail
from finances.models import Account
from rest_framework import status


class AccountAPIDetailTest(TestCase):
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

        self.factory = RequestFactory()
        self.account = Account.objects.create(
            name='Conta Corrente',
            balance=100.00
        )

    def test_get(self):
        """
        Testa o método GET para obter a conta específica.

        Este teste verifica se o método GET retorna o status HTTP 200 OK para
        uma solicitação de listagem com detalhes de uma conta válida..
        """

        view = AccountAPIDetail.as_view()
        request = self.factory.get(f'/api/account/{self.account.pk}/')
        response = view(request, pk=self.account.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        """
        Testa o método PATCH para atualizar os dados de uma conta específica.

        Este teste verifica se o método PATCH retorna o status HTTP 200 OK para
        uma solicitação de atualização de conta válida.
        """

        view = AccountAPIDetail.as_view()

        data = {
            'name': 'Conta Poupança',
            'balance': 200.00
        }

        request = self.factory.patch(
            f'/api/account/{self.account.pk}/',
            data=data,
            content_type='application/json'
        )

        response = view(request, pk=self.account.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Testa o método DELETE para exclusão de uma conta específica.

        Este teste verifica se o método DELETE retorna o status HTTP 204 No
        Content para uma solicitação de exclusão de conta válida.
        """

        view = AccountAPIDetail.as_view()
        request = self.factory.delete(f'/api/account/{self.account.pk}/')
        response = view(request, pk=self.account.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

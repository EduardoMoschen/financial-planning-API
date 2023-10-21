from django.test import TestCase, RequestFactory
from finances.views import OnwerAPIDetail
from django.contrib.auth.models import User
from rest_framework import status
from finances.models import Account


class OwnerAPIDetailTest(TestCase):
    """
    Teste para a classe OwnerAPIDetail.

    Esta classe contém testes para os métodos da classe OwnerAPIDetail, que
    lida com operações detalhadas relacionadas a um titular específico.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria uma instância
        inicial de objetos necessários para os testes.
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

    def test_get(self):
        """
        Testa o método GET para obter o titular específico.

        Este teste verifica se o método GET retorna o status HTTP 200 OK para
        uma solicitação de listagem com detalhes de um titular válido.
        """

        view = OnwerAPIDetail.as_view()
        request = self.factory.get(f'/api/owner/{self.user.pk}/')
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        """
        Testa o método PATCH para atualizar os dados do titular específico.

        Este teste verifica se o método PATCH retorna o status HTTP 200 OK para
        uma solicitação de atualização com os dados válidos do titular.
        """

        view = OnwerAPIDetail.as_view()

        data = {
            'email': 'calosalberto@email.com'
        }

        request = self.factory.patch(
            f'/api/owner/{self.user.pk}/',
            data=data,
            content_type='application/json'
        )

        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Testa o método DELETE para exclusão do titular específico.

        Este teste verifica se o método DELETE retorna o status HTTP 204 NO
        CONTENT para uma solicitação de exclusão válida do titular e conta
        associada.
        """

        view = OnwerAPIDetail.as_view()
        request = self.factory.delete(f'/api/owner/{self.user.pk}/')
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(owner=self.user).exists())

    def test_delete_owner_without_account(self):
        """
        Testa o método DELETE para quando o titular não tiver uma conta.

        Este teste verifica se o método DELETE retorna o status HTTP 204 NO
        CONTENT para uma solicitação de exclusão válida quando ocorrer apenas
        a exclusão do titular sem uma conta associada a ele.
        """

        view = OnwerAPIDetail.as_view()

        user_without_account = User.objects.create_user(
            username='user_without_account',
            password='password123',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com'
        )

        request = self.factory.delete(f'/api/owner/{user_without_account.pk}/')

        response = view(request, pk=user_without_account.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Account.objects.filter(
            owner=user_without_account).exists())

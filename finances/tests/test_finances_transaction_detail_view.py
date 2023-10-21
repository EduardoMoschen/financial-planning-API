from django.test import TestCase, RequestFactory
from finances.views import TransactionAPIDetail
from finances.models import Transaction, Account, Category, Budget
from rest_framework import status
from django.contrib.auth.models import User


class TransactionAPIDetailTest(TestCase):
    """
    Teste para a classe TransactionAPIDetail.

    Esta classe contém testes para os métodos da classe TransactionAPIDetail,
    que lida com operações detalhadas relacionadas à uma transação específica.
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

        self.category_1 = Category.objects.create(
            name='Academia'
        )

        self.category_2 = Category.objects.create(
            name="Medicamentos"
        )

        self.transaction = Transaction.objects.create(
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

    def test_get(self):
        """
        Testa o método GET para obter a transação específica.

        Este teste verifica se o método GET retorna o status HTTP 200 OK para
        uma solicitação de listagem com detalhes de uma transação específica.
        """

        view = TransactionAPIDetail.as_view()
        request = self.factory.get(f'/api/transaction/{self.transaction.pk}/')
        response = view(request, pk=self.transaction.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        """
        Testa o método PUT para atualizar os dados da transação específica.

        Este teste verifica se o método PUT retorna o status HTTP 200 OK para
        uma solicitação de atualização com os dados válidos da transação.
        """

        view = TransactionAPIDetail.as_view()

        data = {
            'amount': 180,
            'description': 'Compra de remédios na farmácia.',
            'account': self.account.pk,
            'category': self.category_1.pk
        }

        request = self.factory.put(
            f'/api/transaction/{self.transaction.pk}/',
            data=data,
            content_type='application/json'
        )

        response = view(request, pk=self.transaction.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Testa o método DELETE para exclusão da transação específica.

        Este teste verifica se o método DELETE retorna o status HTTP 204 NO
        CONTENT para uma solicitação de exclusão válida da transação. Caso haja
        uma categoria associada junto ao orçamento, o valor 'spent' do
        orçamento é decrementado do valor da transação excluída.
        """

        view = TransactionAPIDetail.as_view()

        request = self.factory.delete(
            f'/api/transaction/{self.transaction.pk}/'
        )

        response = view(request, pk=self.transaction.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(pk=self.transaction.pk)

        category = self.transaction.category
        if category.budget_set.exists():
            budget = category.budget_set.first()
            self.assertEqual(budget.spent, 0)

    def test_delete_non_existent_transaction(self):
        """
        Teste para o método DELETE para exclusão de uma transação não
        cadastrada.

        Este teste verifica se o método DELETE retorna o status HTTP 404 NOT
        FOUND após uma solicitação de exclusão de uma transação não existente.
        """

        view = TransactionAPIDetail.as_view()

        non_existent_transaction_id = self.transaction.pk + 100

        request = self.factory.delete(
            f'/api/transaction/{non_existent_transaction_id}/')
        response = view(request, pk=non_existent_transaction_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_budget(self):
        """
        Testa o método DELETE para exclusão de uma transação específica que
        tenha um orçamento associado.

        Este teste verifica se o método DELETE retorna o status HTTP 204 NO
        CONTENT para uma solicitação de exclusão válida, além de atualizar o
        valor dos campos do orçamento.
        """

        request = self.factory.delete(
            f'/api/transaction/{self.transaction.pk}/'
        )

        view = TransactionAPIDetail()

        self.transaction.category = self.category_1
        self.transaction.save()

        new_budget = Budget.objects.create(
            start_date='2023-08-01',
            end_date='2023-08-31',
            amount=self.transaction.amount,
            account=self.account,
            category=self.category_1,
            spent=self.transaction.amount
        )

        response = view.delete(request, pk=self.transaction.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(pk=self.transaction.pk)

        self.category_1.refresh_from_db()
        new_budget.refresh_from_db()
        self.assertEqual(new_budget.spent, 0)

    def test_delete_without_budget(self):
        """
        Testa o método DELETE para exclusão de uma transação específica que não
        tenha um orçamento associado.

        Este teste verifica se o método DELETE retorna o status HTTP 204 NO
        CONTENT após a solicitação de exclusão válida de uma transação sem um
        orçamento associado a ela.
        """

        request = self.factory.delete(
            f'/api/transaction/{self.transaction.pk}/'
        )

        view = TransactionAPIDetail()

        self.transaction.category = None
        self.transaction.save()

        response = view.delete(request, pk=self.transaction.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(pk=self.transaction.pk)

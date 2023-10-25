from django.test import TestCase
from django.contrib.auth.models import User
from finances.models import Account, Category, Budget, Transaction
from finances.serializers import TransactionSerializer
from rest_framework.exceptions import ValidationError


class TransactionSerializerTestCase(TestCase):
    """
    Testes para o serializador de Transação.

    Esta classe contém testes para o serializador de Transaction, que é
    responsável por validar e transformar dados de transações financeiras em um
    formato adequado para o uso na API.
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
            name='Conta Corrente',
            balance=1000
        )

        self.category_1 = Category.objects.create(
            name='Academia'
        )

        self.category_2 = Category.objects.create(
            name="Medicamentos"
        )

        self.transaction_data = {
            'amount': 30,
            'description': 'Test Transaction',
            'account': self.account.pk,
            'category': self.category_1.pk
        }

        self.serializer = TransactionSerializer()

    def test_amount_required(self):
        """
        Testa a necessidade de uma quantia.

        Este teste verifica se o serializador valida corretamente a presença de
        uma quantia e lança um erro se ela estiver ausente.
        """

        with self.assertRaises(ValidationError) as context:
            data = {'description': 'Test', 'account': 'acc', 'category': 'cat'}
            TransactionSerializer().validate(data)
        self.assertTrue('amount' in context.exception.detail)

    def test_description_required(self):
        """
        Testa a necessidade de uma descrição.

        Este teste verifica se o serializador valida corretamente a presença de
        uma descrição e lança um erro se ela estiver ausente.
        """

        with self.assertRaises(ValidationError) as context:
            data = {'amount': 100, 'account': 'acc', 'category': 'cat'}
            TransactionSerializer().validate(data)
        self.assertTrue('description' in context.exception.detail)

    def test_account_required(self):
        """
        Testa a necessidade de uma conta.

        Este teste verifica se o serializador valida corretamente a presença de
        uma conta e lança um erro se ela estiver ausente.
        """

        with self.assertRaises(ValidationError) as context:
            data = {'amount': 100, 'description': 'Test', 'category': 'cat'}
            TransactionSerializer().validate(data)
        self.assertTrue('account' in context.exception.detail)

    def test_category_required(self):
        """
        Testa a necessidade de uma categoria.

        Este teste verifica se o serializador valida corretamente a presença de
        uma categoria e lança um erro se ela estiver ausente.
        """

        with self.assertRaises(ValidationError) as context:
            data = {'amount': 100, 'description': 'Test', 'account': 'acc'}
            TransactionSerializer().validate(data)
        self.assertTrue('category' in context.exception.detail)

    def test_insufficient_balance(self):
        """
        Testa o saldo insuficiente.

        Este teste verifica se o serializador valida corretamente um saldo
        insuficiente e lança um erro apropriado.
        """

        data = {
            'amount': 500,
            'description': 'Test',
            'account': {'balance': 200},
            'category': 'cat'

        }

        serializer = TransactionSerializer()
        account = data['account']
        account_obj = Account.objects.create(balance=account['balance'])
        data['account'] = account_obj

        with self.assertRaises(ValidationError) as context:
            serializer.validate(data)
        self.assertTrue(
            'Insufficient balance for the transaction.' in
            str(context.exception)
        )

    def test_create_method(self):
        """
        Testa o método de criação.

        Este teste verifica se o método de criação do serializador cria
        corretamente uma nova transação com os dados fornecidos.
        """

        serializer = TransactionSerializer(data=self.transaction_data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        self.assertEqual(transaction.amount, self.transaction_data['amount'])

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 970)

    def test_create_method_exceeds_budget(self):
        """
        Testa o método de criação que excede o orçamento.

        Este teste verifica se o método de criação do serializador lança um
        erro ao tentar exceder o orçamento permitido.
        """

        budget = Budget.objects.create(  # noqa: 841
            start_date='2023-08-01',
            end_date='2023-08-31',
            amount=100,
            account=self.account,
            category=self.category_1
        )

        transaction_data_exceeds_budget = {
            'amount': 150,
            'description': 'Exceeding Transaction',
            'account': self.account.pk,
            'category': self.category_1.pk
        }

        serializer = TransactionSerializer(
            data=transaction_data_exceeds_budget
        )

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        errors = context.exception.detail
        message = 'The value of the transaction exceeds the \
budget for this category.'
        self.assertIn(
            message,
            errors.get('non_field_errors', [''])
        )

    def test_update_transaction(self):
        """
        Testa o método de atualização de transação.

        Este teste verifica se o método de atualização do serializador atualiza
        corretamente uma transação com os novos dados fornecidos.
        """

        account = Account.objects.create(balance=1000)
        category = Category.objects.create(
            name='Test Category')
        budget = Budget.objects.create(
            account=account,
            category=category,
            amount=500,
            start_date='2023-01-01',
            end_date='2023-01-31'
        )

        transaction_data = {
            'amount': 200,
            'description': 'Initial transaction',
            'account': account,
            'category': category
        }

        transaction = Transaction.objects.create(**transaction_data)

        serializer = TransactionSerializer()
        updated_transaction_data = {
            'amount': 300,
            'description': 'Updated transaction',
            'category': category
        }

        serializer.update(transaction, updated_transaction_data)

        updated_transaction = Transaction.objects.get(pk=transaction.id)
        self.assertEqual(updated_transaction.amount, 300)
        self.assertEqual(
            updated_transaction.description,
            'Updated transaction'
        )

        updated_budget = Budget.objects.get(pk=budget.id)
        self.assertEqual(updated_budget.spent, 300 - 200)

        updated_account = Account.objects.get(pk=account.id)
        self.assertEqual(updated_account.balance, 1000)

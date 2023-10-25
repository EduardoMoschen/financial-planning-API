from django.test import TestCase
from finances.serializers import BudgetSerializer
from finances.models import Budget, Account, Category
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.exceptions import ValidationError


class BudgetSerializerTestCase(TestCase):
    """
    Testes para o serializador de Orçamento.

    Esta classe contém testes para o serializador de Budget, que é responsável
    por validar e transformar dados de orçamentos financeiros em um formato
    adequado para o uso na API.
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

        start_date_1 = datetime.strptime('2023-10-01', '%Y-%m-%d').date()
        end_date_1 = datetime.strptime('2023-10-10', '%Y-%m-%d').date()

        self.budget_1 = Budget.objects.create(
            start_date=start_date_1,
            end_date=end_date_1,
            amount=150,
            account=self.account,
            category=self.category_1
        )

    def test_account_required(self):
        """
        Testa a necessidade de uma conta.

        Este teste verifica se o serializador valida corretamente a presença de
        uma conta e lança um erro se ela estiver ausente.
        """

        with self.assertRaises(ValidationError):
            data = {
                'category': 'cat',
                'amount': 500,
                'start_date': '2023-01-01',
                'end_date': '2023-01-31'
            }
            BudgetSerializer().validate(data)

    def test_category_required(self):
        """
        Testa a necessidade de uma categoria.

        Este teste verifica se o serializador valida corretamente a presença de
        uma categoria e lança um erro se ela estiver ausente.
        """

        with self.assertRaises(ValidationError):
            data = {
                'account': 'acc',
                'amount': 500,
                'start_date': '2023-01-01',
                'end_date': '2023-01-31'
            }
            BudgetSerializer().validate(data)

    def test_amount_required(self):
        """
        Testa a necessidade de uma quantia.

        Este teste verifica se o serializador valida corretamente a presença de
        uma quantia e lança um erro se ela estiver ausente.
        """

        with self.assertRaises(ValidationError):
            data = {
                'account': 'acc',
                'category': 'cat',
                'start_date': '2023-01-01',
                'end_date': '2023-01-31'
            }
            BudgetSerializer().validate(data)

    def test_update_method(self):
        """
        Testa o método de atualização.

        Este teste verifica se o método de atualização do serializador atualiza
        corretamente as instâncias de orçamento com os novos dados fornecidos.
        """

        budget_instance = Budget.objects.create(
            account=self.account,
            category=self.category_1,
            amount=100,
            start_date='2023-01-01',
            end_date='2023-01-31'
        )

        valid_data = {
            'account': self.account.id,
            'category': self.category_1.id,
            'amount': 200,
            'start_date': '2023-02-01',
            'end_date': '2023-02-28'
        }

        serializer = BudgetSerializer(
            instance=budget_instance,
            data=valid_data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        updated_instance = serializer.save()

        self.assertEqual(updated_instance.account, self.account)
        self.assertEqual(updated_instance.category, self.category_1)
        self.assertEqual(updated_instance.amount, 200)
        self.assertEqual(
            updated_instance.start_date.strftime('%Y-%m-%d'),
            '2023-02-01'
        )
        self.assertEqual(
            updated_instance.end_date.strftime('%Y-%m-%d'),
            '2023-02-28'
        )

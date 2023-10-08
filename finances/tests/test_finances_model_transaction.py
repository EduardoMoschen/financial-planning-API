from django.test import TestCase
from finances.models import Transaction, Account, Category
from django.contrib.auth.models import User


class TransactionModelTestCase(TestCase):
    def test_transaction_str_with_expected_output(self):
        user = User.objects.create(
            username="user1",
            password="password1",
            first_name="Carlos",
            last_name="Alberto",
            email="carlos@email.com"
        )

        account = Account.objects.create(
            owner=user,
            name="Current Account",
            balance=10000
        )

        category = Category.objects.create(name="Food")

        transaction = Transaction.objects.create(
            account=account,
            category=category,
            amount=250,
            description='Shopping at the supermarket for the weekend'
        )

        expected_output = f'Value: {transaction.amount} - '\
            f'Description: {transaction.description}'

        self.assertEqual(str(transaction), expected_output)

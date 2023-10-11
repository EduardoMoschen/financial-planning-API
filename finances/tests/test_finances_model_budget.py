from django.test import TestCase
from finances.models import Account, Category, Transaction, Budget
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class BudgetModelTestCase(TestCase):
    def test_budget_str_with_expected_output(self):
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

        start_date = timezone.make_aware(datetime(2023, 1, 1))
        end_date = timezone.make_aware(datetime(2023, 1, 31))

        budget = Budget.objects.create(
            account=account,
            category=category,
            amount=1000,
            start_date=start_date,
            end_date=end_date,
            spent=0,
        )

        expected_output = f'Budget to {budget.category.name} - '\
            f'{budget.amount}'
        self.assertEqual(str(budget), expected_output)

    def test_update_spent(self):
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

        start_date = timezone.make_aware(datetime(2023, 1, 1))
        end_date = timezone.make_aware(datetime(2023, 1, 31))

        budget = Budget.objects.create(
            account=account,
            category=category,
            amount=1000,
            start_date=start_date,
            end_date=end_date,
            spent=0,
        )

        transaction = Transaction.objects.create(
            account=account,
            category=category,
            amount=250.00,
            date=timezone.make_aware(datetime(2023, 1, 15)),
            description='Shopping at the supermarket',
        )

        budget.update_spent(transaction.amount)
        updated_budget = Budget.objects.get(pk=budget.pk)
        self.assertEqual(updated_budget.spent, 250)

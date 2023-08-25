from rest_framework.response import Response
from finances.models import Account, Category, Transaction, Budget
from finances.serializers import (
    AccountSerializer,
    OwnerSerializer,
    CategorySerializer,
    TransactionSerializer,
    BudgetSerializer
)
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class AccountAPIList(APIView):
    def get(self, request):
        accounts = Account.objects.all()

        if not accounts.exists():
            return Response({'message': 'There are no registred accounts.'})

        serializer = AccountSerializer(
            instance=accounts,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class AccountAPIDetail(APIView):
    def get_account(self, pk):
        account = get_object_or_404(
            Account.objects.all(),
            pk=pk
        )

        return account

    def get(self, request, pk):
        account = self.get_account(pk)
        serializer = AccountSerializer(
            instance=account,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)

    def patch(self, request, pk):
        account = self.get_account(pk)
        serializer = AccountSerializer(
            instance=account,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        account = self.get_account(pk)
        account.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OwnerAPIList(APIView):
    def get(self, request):
        owners = User.objects.all()

        if not owners.exists():
            return Response({'message': 'There are no registred owners.'})

        serializer = OwnerSerializer(
            instance=owners,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = OwnerSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        owner = User.objects.create_user(**serializer.validated_data)

        return Response(
            OwnerSerializer(instance=owner).data,
            status=status.HTTP_201_CREATED
        )


class OnwerAPIDetail(APIView):
    class FieldValidator:
        def validate(self, owner, value):
            pass

    class UsernameValidator(FieldValidator):
        def validate(self, owner, value):
            owner.username = value
            owner.save()

    class FirstNameValidator(FieldValidator):
        def validate(self, owner, value):
            owner.first_name = value
            owner.save()

    class LastNameValidator(FieldValidator):
        def validate(self, owner, value):
            owner.last_name = value
            owner.save()

    class EmailValidator(FieldValidator):
        def validate(self, owner, value):
            owner.email = value
            owner.save()

    class PasswordValidator(FieldValidator):
        def validate(self, owner, value):
            owner.password = make_password(value)
            owner.save()

    def get_owner(self, pk):
        owner = get_object_or_404(
            User.objects.all(),
            pk=pk
        )

        return owner

    def get(self, request, pk):
        owner = self.get_owner(pk)
        serializer = OwnerSerializer(
            instance=owner,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)

    def patch(self, request, pk):
        owner = self.get_owner(pk)
        serializer = OwnerSerializer(
            instance=owner,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            field_validators = {
                'username': self.UsernameValidator(),
                'first_name': self.FirstNameValidator(),
                'last_name': self.LastNameValidator(),
                'email': self.EmailValidator(),
                'password': self.PasswordValidator()
            }

            for field, value in serializer.validated_data.items():
                if field in field_validators:
                    field_validators[field].validate(owner, value)
                else:
                    return Response(
                        {'error': f'invalid field: {field}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        owner = self.get_owner(pk)

        try:
            account = Account.objects.get(owner=owner)
            account.delete()
        except Account.DoesNotExist:
            pass

        owner.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryAPIList(APIView):
    def get(self, request):
        categories = Category.objects.all()

        if not categories.exists():
            return Response({'message': 'There are no registred categories.'})

        serializer = CategorySerializer(
            instance=categories,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class CategoryAPIDetail(APIView):
    def get_category(self, pk):
        category = get_object_or_404(
            Category.objects.all(),
            pk=pk
        )

        return category

    def get(self, request, pk):
        category = self.get_category(pk)
        serializer = CategorySerializer(
            instance=category,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_category(pk)
        serializer = CategorySerializer(
            instance=category,
            data=request.data,
            many=False,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        category = self.get_category(pk)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionAPIList(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()

        if not transactions.exists():
            return Response(
                {'message': 'There are no regristred transactions.'}
            )

        serializer = TransactionSerializer(
            instance=transactions,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionAPIDetail(APIView):
    def get_transaction(self, pk):
        transactions = get_object_or_404(
            Transaction.objects.all(),
            pk=pk
        )

        return transactions

    def get(self, request, pk):
        transaction = self.get_transaction(pk)
        serializer = TransactionSerializer(
            instance=transaction,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)

    def patch(self, request, pk):
        transaction = self.get_transaction(pk)
        serializer = TransactionSerializer(
            instance=transaction,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        transaction = self.get_transaction(pk)
        transaction.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BudgetAPIList(APIView):
    def get(self, request):
        budgets = Budget.objects.all()

        if not budgets.exists():
            return Response(
                {'message': 'There are no registred budgets.'}
            )

        serializer = BudgetSerializer(
            instance=budgets,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BudgetAPIDetail(APIView):
    def get_budget(self, pk):
        budget = get_object_or_404(
            Budget.objects.all(),
            pk=pk
        )

        return budget

    def get(self, request, pk):
        budget = self.get_budget(pk)
        serializer = BudgetSerializer(
            instance=budget,
            many=False,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

    def patch(self, request, pk):
        budget = self.get_budget(pk)
        serializer = BudgetSerializer(
            instance=budget,
            many=False,
            context={'request': request},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        budget = self.get_budget(pk)
        budget.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.response import Response
from finances.models import Account, Category, Transaction
from finances.serializers import (
    AccountSerializer,
    OwnerSerializer,
    CategorySerializer,
    TransactionSerializer
)
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import User


class BaseDetailAPI(APIView):
    def patch(self, request, pk):
        instance = self.get_instance(pk)
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            many=False,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get_instance(self, pk):
        raise NotImplementedError(
            'Subclasses must implement get_instance method.'
        )

    def get_serializer(self, instance, data, **kwargs):
        raise NotImplementedError(
            'Subclasses must implement get_instance method.'
        )


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


class AccountAPIDetail(BaseDetailAPI):
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

    def get_instance(self, pk):
        return get_object_or_404(Account.objects.all(), pk=pk)

    def get_serializer(self, instance, data, **kwargs):
        return AccountSerializer(
            instance=instance,
            data=data,
            **kwargs
        )

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


class OnwerAPIDetail(BaseDetailAPI):
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

    def get_instance(self, pk):
        return get_object_or_404(User.objects.all(), pk=pk)

    def get_serializer(self, instance, data, **kwargs):
        return OwnerSerializer(
            instance=instance,
            data=data,
            **kwargs
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

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

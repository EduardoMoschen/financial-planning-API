from rest_framework.response import Response
from finances.models import Account
from finances.serializers import AccountSerializer, OwnerSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import User


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
            status=status.HTTP_201_CREATED)


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
            context={'request': request}
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
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class OnwerAPIDetail(APIView):
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
            context={}
        )

        return Response(serializer.data)

    def patch(self, request, pk):
        owner = self.get_owner(pk)
        serializer = OwnerSerializer(
            instance=owner,
            data=request.data,
            many=False,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        owner = self.get_owner(pk)
        owner.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

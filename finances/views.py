from rest_framework.response import Response
from rest_framework.decorators import api_view
from finances.models import Account
from finances.serializers import AccountSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(['get', 'post'])
def accounts_list(request):
    if request.method == 'GET':
        accounts = Account.objects.all()

        if not accounts.exists():
            return Response({'message': 'There are no registred accounts.'})

        serializer = AccountSerializer(
            instance=accounts,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
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


@api_view(['get'])
def account_detail(request, pk):
    account = get_object_or_404(
        Account.objects.all(),
        pk=pk
    )

    if request.method == 'GET':
        serializer = AccountSerializer(
            instance=account,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)

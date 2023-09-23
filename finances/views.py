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


class AccountAPIList(APIView):
    """
    Representação da API para gerenciar contas financeiras dos usuários.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get: Retorna uma lista de todas as contas financeiras registradas.
        post: Cria uma nova conta financeira.

    Endpoint Base:
        /api/accounts/
    """

    def get(self, request):
        """
        Método HTTP GET para listar todas as contas registradas.

        Parâmetros:
            request: O objeto de solicitação HTTP.

        Exemplo de Uso:
            GET /api/accounts/

        Exemplo de Resposta JSON:
            [
                {
                    "id": 1,
                    "name": "Tipo_de_Conta",
                    "balance": "850.00",
                    "created_at": "2023-08-16T15:44:33.227307-03:00",
                    "owner": 1
                },
                {
                    "id": 2,
                    "name": "Outro_Tipo_de_Conta",
                    "balance": "750.00",
                    "created_at": "2023-08-19T19:58:43.550259-03:00",
                    "owner": 2
                }
            ]

        Retorna:
            Response: Uma resposta HTTP contendo uma lista de contas em formato
            JSON.
        """

        # Obtém todas as contas que estão registradas para listar.
        accounts = Account.objects.all()

        # Verifica se não há contas registradas.
        if not accounts.exists():
            return Response({'message': 'There are no registred accounts.'})

        # Serializa a lista de contas em formato JSON.
        serializer = AccountSerializer(
            instance=accounts,
            many=True,
            context={'request': request}
        )

        # Retorna a lista de contas serializadas como resposta.
        return Response(serializer.data)

    def post(self, request):
        """
        Método HTTP POST para criar uma nova conta.
        Envia os dados da nova conta em formato JSON no corpo da solicitação.

        Parâmetros:
            request: O objeto de solicitação HTTP.

        Exempo de Uso:
            POST /api/accounts/

        Exemplo Request Body:
            {
                "name": "Tipo_de_Conta",
                "balance": 1000,
                "owner": 1
            }

        Retorna:
            Response: Uma resposta HTTP com status 201 Created como
            confirmação. Os detalhes da nova contasão retornados no corpo da
            resposta em formato JSON.
        """

        # Serializa os dados para a criação da conta com base na solicitação do
        # usuário.
        serializer = AccountSerializer(
            data=request.data,
            context={'request': request}
        )

        # Verifica se os dados da conta são válidos antes de criar uma nova
        # conta.
        serializer.is_valid(raise_exception=True)

        # Salva a nova conta no banco de dados para manter o registro.
        serializer.save()

        # Retorna os dados da nova conta criada com status 201 Created como
        # confirmação.
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class AccountAPIDetail(APIView):
    """
    Representação da API que lida com operações detalhadas relacionadas a uma
    conta financeira específica do usuário.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get_account: Obtém uma conta financeira específica com base no ID.
        get: Retorna detalhes de uma conta financeira específica.
        patch_balance: Atualiza valor monetário de uma conta financeira
        específica.
        delete: Exclui uma conta financeira específica.

    Endpoint Base:
        /api/account/<pk>/
    """

    def get_account(self, pk):
        """
        Método auxiliar para obter uma conta financeira com base no ID.

        Parâmetros:
            pk: O ID da conta a ser obtida.

        Retorna:
            Account: A conta financeira encontrada com base no ID fornecido.

        Exemplo de Uso:
            account = self.get_account(1)
        """

        # Obtém uma conta específica com base no ID fornecido.
        account = get_object_or_404(
            Account.objects.all(),
            pk=pk
        )

        # Retorna a conta financeira encontrada.
        return account

    def get(self, request, pk):
        """
        Método HTTP GET para obter detalhes de uma conta financeira específica.

        Parâmetros:
            request: O objeto de solicitação HTTP.
            pk: O ID da conta a ser obtida.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes da conta em
            formato JSON.
        """

        # Obtém a conta específica com base no ID fornecido.
        account = self.get_account(pk)

        # Serializa o titular da conta.
        owner_serializer = OwnerSerializer(account.owner)

        # Serializa as transações relacionadas a essa conta.
        transactions = account.transaction_set.all()
        transaction_serializer = TransactionSerializer(transactions, many=True)

        # Serializa os budgets relacionados a essa conta.
        budgets = account.budget_set.all()
        budget_serializer = BudgetSerializer(budgets, many=True)

        # Retorna os dados da conta serializados como resposta.
        return Response({
            'owner': owner_serializer.data,
            'transactions': transaction_serializer.data,
            'budgets': budget_serializer.data
        })

    def patch_balance(self, request, pk):
        """
        Método HTTP PATCH para atualziar o saldo de uma conta financeira
        específica.

        Parâmetros:
            request: O objeto de solicitação contendo os dados a serem
            atualizados.
            pk: O ID da conta a ser atualizada.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes da conta
            atualizada em formato JSON.
        """

        # Obtém a conta específica com base no ID fornecido.
        account = self.get_account(pk)

        # Serializa os dados da conta a ser atualizada com base na solicitação
        # do usuário. No caso, da solicitação para atualizar o saldo.
        serializer = AccountSerializer(
            instance=account,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True  # Permite atualizações parciais.
        )

        # Verifica se os dados da conta são válidos antes de atualizar a conta.
        serializer.is_valid(raise_exception=True)

        # Salva as atualizações da conta no banco de dados.
        serializer.save()

        # Retorna os detalhes da conta atualizada.
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Método HTTP DELETE para excluir uma conta financeira específica.

        Parâmetros:
            request: O objeto de solicitação HTTP.
            pk: O ID da conta a ser excluída.

        Retorna:
            Response: Uma resposta HTTP com status 204 No Content como
            confirmação.
        """

        # Obtém a conta específica com base no ID fornecido.
        account = self.get_account(pk)

        # Remove a conta do banco de dados.
        account.delete()

        # Retrona uma resposta vazia com status 204 No Content como
        # confirmação.
        return Response(status=status.HTTP_204_NO_CONTENT)


class OwnerAPIList(APIView):
    """
    Representação da API para gerar titulares das contas financeiras.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get: Retorna uma lista de todos os titulares registrados.
        post: Cria um novo titular.

    Endpoint Base:
        /api/owners/
    """

    def get(self, request):
        """
        Método HTTP GET para listar todo os titulares registrados.

        Parâmetros:
            request: O objeto da solicitação HTTP.

        Exemplo de Uso:
            GET /api/owners/

        Exemplo de Resposta JSON:
            [
                {
                    "id": 1,
                    "username": "Username_do_Titular",
                    "first_name": "Nome",
                    "last_name": "Sobrenome",
                    "email": "E-mail"
                },
                {
                    "id": 2,
                    "username": "Username_do_Titular",
                    "first_name": "Nome",
                    "last_name": "Sobrenome",
                    "email": "E-mail"
                },
            ]

        Retorna:
            Response: Uma resposta HTTP contendo uma lista dos titulares em
            formato JSON.
        """

        # Obtém todos os titulares que estão registrados para listagem.
        owners = User.objects.all()

        # Verifica se não há titulares registrados.
        if not owners.exists():
            return Response({'message': 'There are no registred owners.'})

        # Serializa a lista de titulares em formato JSON.
        serializer = OwnerSerializer(
            instance=owners,
            many=True,
            context={'request': request}
        )

        # Retorna a lista de titulares serializados como resposta.
        return Response(serializer.data)

    def post(self, request):
        """
        Método HTTP PST para criar um novo titular.
        Envia os dados do novo titular em formato JSON no corpo da solicitação.

        Parâmetros:
            request: O objeto de solicitação HTTP.

        Exemplos de Uso:
            POST /api/owners/

        Exemplo de Request Body:
            {
                "username": "Username",
                "first_name": "Nome",
                "last_name": "Sobrenome",
                "email": "E-mail"
            }

        Retorna:
            Response: Uma resposta HTTP com status 201 Created como
            confirmação. Os detalhes do novo titular são retornados no corpo da
            resposta em formato JSON.

        Erros:
            Se os dados enviados no corpo da solicitação forem inválidos, uma
            resposta HTTP com status 400 Bad Request é retornada, contendo
            informações detalhadas sobre os erros.
        """

        # Serializa os dados para a criação do novo titular com base na
        # solicitação do usuário.
        serializer = OwnerSerializer(
            data=request.data,
            context={'request': request}
        )

        # Verifica se os dados do titular são válidos antes de criar um novo
        # titular.
        if serializer.is_valid():

            # Cria um novo titular com base nos dados validados.
            owner = User.objects.create_user(**serializer.validated_data)

            # Retorna os detalhes do novo titular criado com status 201 Created
            # como confirmação.
            return Response(
                OwnerSerializer(instance=owner).data,
                status=status.HTTP_201_CREATED
            )

        # Se os dados forem inválidos, retorna uma resposta com status 400 Bad
        # Request contendo informações detalhadas sobre os erros.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnwerAPIDetail(APIView):
    """
    Representação da API que lida com operações detalhadas relacionadas a um
    titular específico.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get_owner: Obtém um titula específico com base no iD.
        get: Retorna detalhes de um titular específico.
        patch: Atualiza campos de forma parcial, ou total, de um titular
        específico.
        delete: Exclui um titular específico junto com a(s) conta(s)
        associada(s) à ele.

    Endpoint Base:
        /api/owner/<pk>/
    """

    def get_owner(self, pk):
        """
        Método auxiliar para obter um titular com base no ID.

        Parâmetros:
            pk: O ID do titular a ser obtido.

        Retorna:
            Owner: O titular enconrtrado com base no ID fornecido.

        Exemplo de Uso:
            owner = self.get_owner(1)
        """

        # Obtém um titular específico com base no ID fornecido.
        owner = get_object_or_404(
            User.objects.all(),
            pk=pk
        )

        # Retorna o titular encontrado.
        return owner

    def get(self, request, pk):
        """
        Método HTTP GET para obter detalhes de um titular específico.

        Parâmetros:
            request: O objeto de solicitação HTTP.
            pk: O ID do titular a ser obtido.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes do titular em
            formato JSON.
        """

        # Obtém o titular específico com base no ID fornecido.
        owner = self.get_owner(pk)

        # Serializa os detahes do titular em formato JSON para listagem.
        serializer = OwnerSerializer(
            instance=owner,
            many=False,
            context={'request': request}
        )

        # Retorna os dados da conta serializados como resposta.
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Método HTTP PATCH para atualizar os dados de um titular específico.

        Parâmetros:
            request: O objeto de solicitação contendo os dados a serem
            atualizados.
            pk: O ID do titular a ser atualizado.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes do titular
            atualizada em formato JSON.
        """

        # Obtém o titular específico com base no ID fornecido.
        owner = self.get_owner(pk)

        # Serializa os dados do titular a ser atualizado com base na
        # solicitação do usuário. A atualização é feita de forma parcial.
        serializer = OwnerSerializer(
            instance=owner,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )

        # Verifica se os dados do titular são válidos antes de atualizar.
        serializer.is_valid(raise_exception=True)

        # Salva a atualização do titular no banco de dados.
        serializer.save()

        # Retorna os detalhes do titular atualizados.
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Método HTTP DELETE para excluir um titular específico e, caso tenha uma
        conta associada a ele, será excluída.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID do titular a ser excluído.

        Retorna:
            Response: Uma resposta HTTP com status 204 No Content como
            confirmação.
        """

        # Obtém o titular específico com base no ID fornecido.
        owner = self.get_owner(pk)

        try:
            # Obtém a conta associada ao titular, se existir.
            account = Account.objects.get(owner=owner)

            # Remove a conta associada ao titular.
            account.delete()
        except Account.DoesNotExist:
            # Caso não exista a conta, ignora a exceção.
            pass

        # Remove o titular do banco de dados.
        owner.delete()

        # Retorna uma resposta vazia com status 204 No Content como
        # confirmação.
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryAPIList(APIView):
    """
    Representação da API para gerenciar categorias de gastos.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get: Retorna uma lista de todas as categorias registradas.
        post: Cria uma nova categoria.

    Endpoint Base:
        /api/categories/
    """

    def get(self, request):
        """
        Método HTTP GET para listar todas as categorias registradas.

        Parâmetros:
            request: O objeto da solicitação HTTP.

        Exemplo de Uso:
            GET /api/categories/

        Exemplo de Resposta JSON:
            [
                {
                    "id": 1,
                    "name": "Nome_da_Categoria",
                },
                {
                    "id": 2,
                    "name": "Nome_da_Categoria",
                },
            ]

        Retorna:
            Response: Uma resposta HTTP contendo uma lista de categorias em
            formato JSON.
        """

        # Obtém todas as categorias registradas para listagem.
        categories = Category.objects.all()

        # Verifica se não há categorias registradas.
        if not categories.exists():
            return Response({'message': 'There are no registred categories.'})

        # Serializa a lista de categorias em formato JSON.
        serializer = CategorySerializer(
            instance=categories,
            many=True,
            context={'request': request}
        )

        # Retorna a lista de categorias serializadas como resposta.
        return Response(serializer.data)

    def post(self, request):
        """
        Método HTTP POST para criar uma nova categoria.

        Parâmetros:
            request: O objeto da solicitação HTTP.

        Exemplo de Uso:
            POST /api/categories/

        Exemplo de Request Body:
            {
                "name": "Nome_da_Categoria"
            }

        Retorna:
            Response: Uma resposta HTTP com status 201 Created como
            confirmação. Os detalhes da nova categoria são retornados no corpo
            da resposta em formato JSON.

        Erros:
            Se os dados enviados no corpo da solicitação forem inválidos, uma
            resposta HTTP com status 400 Bad Request é retornada contendo
            informações detalhadas sobre os erros.
        """

        # Serializa os dados para a criação da nova categoria com base na
        # solicitação do usuário.
        serializer = CategorySerializer(
            data=request.data,
            context={'request': request}
        )

        # Verifica se os dados da categoria são válidos antes de criar uma nova
        # categoria.
        if serializer.is_valid():

            # Cria uma nova categoria com base nos dados validados.
            category = serializer.save()

            # Retorna os detalhes da nova categoria criada com status 201
            # Created como confirmação.
            return Response(
                CategorySerializer(instance=category).data,
                status=status.HTTP_201_CREATED
            )

        # Se os dados forem inválidos, retorna uma resposta com status 400 Bad
        # Request contendo informações detalhadas sobre os erros.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAPIDetail(APIView):
    """
    Representação da API que lida com operações detalhadas relacionadas a uma
    categoria específica.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get_category: Obtém uma categoria específica com base no ID.
        get: Retorna detalhes sobre uma categoria específica.
        put: Atualiza o nome da categoria.
        delete: Exclui uma categoria específica.

    Endpoint Base:
        /api/category/<pk>/
    """

    def get_category(self, pk):
        """
        Método auxiliar para obter uma categoria com base no ID.

        Parâmetros:
            pk: O ID da categoria a ser obtida.

        Retorna:
            Category: A categoria encontrada com base no ID fornecido.

        Exemplo de Uso:
            category = self.get_category(1)
        """

        # Obtém a categoria específica com base no ID fornecido.
        category = get_object_or_404(
            Category.objects.all(),
            pk=pk
        )

        # Retorna a categoria encontrada.
        return category

    def get(self, request, pk):
        """
        Método HTTP GET para obter detalhes de uma categoria específica.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID da categoria a ser obtida.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes da categoria em
            formato JSON.
        """

        # Obtém a categoria específica com base no ID fornecido.
        category = self.get_category(pk)

        # Serializa os detalhes da categoria em formato JSON para listagem.
        serializer = CategorySerializer(
            instance=category,
            many=False,
            context={'request': request}
        )

        # Retorna os dados da categoria serializados como resposta.
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Método HTTP PUT para atualizar o nome de uma categoria específica.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID da cateogira a ser obtida.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes da categoria
            atualizida em formato JSON.
        """

        # Obtém a categoria específica com base no ID fornecido.
        category = self.get_category(pk)

        # Serializa os dados da categoria com o nome a ser atualizado com base
        # na solicitação do usuário.
        serializer = CategorySerializer(
            instance=category,
            data=request.data,
            many=False,
            context={'request': request}
        )

        # Verifica se o dado alterado da categoria é válido antes de atualizar.
        serializer.is_valid(raise_exception=True)

        # Salva a atualização da categoria no banco de dados.
        serializer.save()

        # Retorna os detalhes da categoria atualizada.
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Método HTTP DELETE para excluir uma categoria específica.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID da categoria a ser obtida.

        Retorna:
            Response: Uma resposta HTTP com status 204 No Content como
            confirmação.
        """

        # Obtém a categoria específica com base no ID fornecido.
        category = self.get_category(pk)

        # Remove a categoria do banco de dados.
        category.delete()

        # Retorna uma resposta vazia com status 204 No Content como
        # confirmação.
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionAPIList(APIView):
    """
    Representação da API para gerenciar as transações realizadas pelo titular.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get: Retorna uma lista de todas as transações realizadas.
        post: Cria uma nova transação.

    Endpoint Base:
        /api/transactions/
    """

    def get(self, request):
        """
        Método HTTP GET para listar todas as transações registradas.

        Parâmetros:
            request: O objeto da solicitação.

        Exemplo de Uso:
            GET /api/transactions/

        Exemplo de Resposta JSON:
            [
                {
                    "id": 4,
                    "amount": "200.00",
                    "description": "Compra em supermercado",
                    "account": 3,
                    "category": 1
                },
                {
                    "id": 5,
                    "amount": "200.00",
                    "description": "Pagamento de aluguel",
                    "account": 3,
                    "category": 3
                }
            ]

        Retorna:
            Response: Uma resposta HTTP contendo uma lista de transações em
            formato JSON.
        """

        # Obtém todas as transações registradas para listagem.
        transactions = Transaction.objects.all()

        # Verifica se não há transações registradas.
        if not transactions.exists():
            return Response(
                {'message': 'There are no regristred transactions.'}
            )

        # Serializa a lista de transações em formato JSON.
        serializer = TransactionSerializer(
            instance=transactions,
            many=True,
            context={'request': request}
        )

        # Retorna a lista de transações serializadas como resposta.
        return Response(serializer.data)

    def post(self, request):
        """
        Método HTTP POST para criar uma nova transação.
        Envia os dados da nova transação em formato JSON no corpo da
        solicitação.

        Parâmetros:
            request: O objeto da solicitação.

        Exemplo de Uso:
            POST /api/transactions/

        Exemplo de Request Body:
            [
                {
                    "amount": "200.00",
                    "description": "Descrição_da_Transação",
                    "account": 3,
                    "category": 1
                },
            ]

        Retorna:
            Response: Uma resposta HTTP com status 201 Created como
            confirmação. Os detalhes da nova transação são retornados no corpo
            da resposta em formato JSON.
        """

        # Serializa os dados para a criação de uma nova transação com base na
        # solicitação do usuário.
        serializer = TransactionSerializer(
            data=request.data,
            context={'request': request}
        )

        # Verifica se os dados da transação são válidos antes de criar uma nova
        # transação.
        serializer.is_valid(raise_exception=True)

        # Salva a nova transação no banco de dados para manter o registro.
        serializer.save()

        # Retorna os dados da nova transação criada com status 201 Created como
        # confirmação.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionAPIDetail(APIView):
    """
    Representação da API que lida com operações detalhadas relacionadas a uma
    transação específica do titular.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get_transaction: Obtém uma transação específica com base no ID.
        get: Retorna detalhes de uma transação específica.
        patch: Atualiza os dados da transação de forma parcial.
        delete: Exclui uma transação específica.

    Endpoint Base:
        /api/transaction/<pk>/
    """

    def get_transaction(self, pk):
        """
        Método auxilixar para obter uma transação específica com base no ID.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID da categoria a ser obtida.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes da transação em
            formato JSON.
        """

        # Ontém a transação com base no ID fornecido.
        transactions = get_object_or_404(
            Transaction.objects.all(),
            pk=pk
        )

        # Retorna a transação encontrada.
        return transactions

    def get(self, request, pk):
        """
        Método HTTP GET para obter detalhes de uma transação específica.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID da transação a ser obtida.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes da transação em
            formato JSON.
        """

        # Ontém a transação específica com base no ID fornecido.
        transaction = self.get_transaction(pk)

        # Serializa os detalhes da transação em formato JSON para listagem
        serializer = TransactionSerializer(
            instance=transaction,
            many=False,
            context={'request': request}
        )

        # Retorna os dados da transação serializados como resposta.
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Método HTTP PATCH para atualizar os dados de uma transação específica.

        Parâmetros:
            request: O objeto da soicitação HTTP.
            pk: O ID da trasação a ser atualizada.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes da categoria
            atualizada em formato JSON.
        """

        # Ontém a transação espcífica com base no ID fornecido.
        transaction = self.get_transaction(pk)

        # Serializa os dados da transação a ser atualizado com base na
        # solicitação do usuário. A atualização é feita de forma parcial.
        serializer = TransactionSerializer(
            instance=transaction,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )

        # Verifica se os dados da transação são válidos antes de atualizar.
        serializer.is_valid(raise_exception=True)

        # Salva a atualização do titular no banco de dados.
        serializer.save()

        # Retorna os detalhes da transação atualizados.
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Método HTTP DELETE para excluir uma transação específica.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID da transação a ser excluída.

        Retorna:
            Response: Uma resposta HTTP com status 204 No Content como
            confirmação.
        """

        # Obtém a transação específica com base no ID fornecido.
        transaction = self.get_transaction(pk)

        # Remove a transação do banco de dados.
        transaction.delete()

        # Retorna uma resposta vazia com status 204 No Content como
        # confirmação.
        return Response(status=status.HTTP_204_NO_CONTENT)


class BudgetAPIList(APIView):
    """
    Representação da API para gerenciar os orçamentos realizados pelo titular.

    Atributos:
        Nenhum atrbibuto específico nesta classe.

    Métodos:
        get: Obtém uma lista de todos os orçamentos realizados.
        post: Cria um novo orçamento.

    Endpoint Base:
        /api/budgets/
    """

    def get(self, request):
        """
        Método HTTP GET para listar todos os orçamentos registrados.

        Parâmetros:
            request: O objeto da solicitação.

        Exemplo de Uso:
            GET /api/budgets/

        Exemplo de Resposta JSON:
            [
                {
                    "id": 1,
                    "account": 3,
                    "category": 1,
                    "amount": "500.00",
                    "start_date": "2023-08-01",
                    "end_date": "2023-08-31"
                }
            ]

        Retorna:
            Response: Uma resposta HTTP contendo uma lista de orçamentos em
            formato JSON.
        """

        # Obtém todos os orçamentos que estão registrados para listagem.
        budgets = Budget.objects.all()

        # Verifica se não há orçamentos registrados.
        if not budgets.exists():
            return Response({'message': 'There are no registred budgets.'})

        # Serializa a lista de orçamentos em formato JSON.
        serializer = BudgetSerializer(
            instance=budgets,
            many=True,
            context={'request': request}
        )

        # Retorna a lista de orçamentos serializados como resposta.
        return Response(serializer.data)

    def post(self, request):
        """
        Método HTTP POST para criar um novo orçamento.
        Envia os dados do novo orçamento em formato JSON no corpo da
        solicitação.

        Parâmetros:
            request: O objeto da solicitação.

        Exemplo de Uso:
            POST /api/budgets/

        Exemplo de Request Body:
            [
                {
                    "account": 3,
                    "category": 1,
                    "amount": "500.00",
                    "start_date": "Data_de_Início_do_Orçamento",
                    "end_date": "Data_de_Término_do_Orçamento"
                },
            ]

        Retorna:
            Response: Uma resposta HTTP com status 201 Created como
            confirmação. Os detalhes do novo orçamento são retornados no corpo
            da resposta em formato JSON.
        """

        # Serializa os dados para a criação do novo orçamento com base na
        # solicitação do usuário.
        serializer = BudgetSerializer(
            data=request.data,
            context={'request': request}
        )

        # Verifica se os dados do orçamento são válidos antes de criar um novo
        # orçamento.
        serializer.is_valid(raise_exception=True)

        # Salva o novo orçamento no banco de dados para manter o registro.
        serializer.save()

        # Retorna os dados do novo orçamento criado com status 201 Created como
        # \confirmação.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BudgetAPIDetail(APIView):
    """
    Representação da API que lida com operações detalhadas relacionadas a um
    orçamento específico do titular.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        get_budget: Obtém um orçamento específico com base no ID.
        get: Retorna os detalhes de um orçamento específico.
        patch: Atualiza os dados do orçamento de forma parcial.
        delete: Exclui um orçamento específico.
    """

    def get_budget(self, pk):
        """
        Método auxilixar para obter um orçamento específico com base no ID.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID do orçamento a ser obtido.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes do orçamento em
            formato JSON.
        """

        # Obtém o orçamento com base no ID fornecido.
        budget = get_object_or_404(
            Budget.objects.all(),
            pk=pk
        )

        # Retorna o orçamento encontrado.
        return budget

    def get(self, request, pk):
        """
        Método HTTP GET para obter detalhes de um orçamento específico.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID do orçamento a ser obtido.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes do orçamento em
            formato JSON.
        """

        # Obtém o orçamento específico com base no ID fornecido.
        budget = self.get_budget(pk)

        # Serializa os detalhes do orçamento em formato JSON para listagem
        serializer = BudgetSerializer(
            instance=budget,
            many=False,
            context={'request': request}
        )

        # Retorna os dados do orçamento serializados como resposta.
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Método HTTP PATCH para atualizar os dados de um orçamento específico.

        Parâmetros:
            request: O objeto da soicitação HTTP.
            pk: O ID do orçamento a ser obtido.

        Retorna:
            Response: Uma resposta HTTP contendo os detalhes do orçamento
            atualizado em formato JSON.
        """

        # Obtém o orçamento específico com base no ID fornecido.
        budget = self.get_budget(pk)

        # Serializa os dados do orçamento com base na solicitação do usuário. A
        # atualização é feita de forma parcial.
        serializer = BudgetSerializer(
            instance=budget,
            many=False,
            context={'request': request},
            partial=True
        )

        # Verifica se o dado alterado do orçamento é válido antes de atualizar.
        serializer.is_valid(raise_exception=True)

        # Salva a atualização do orçamento atualizado.
        serializer.save()

        # Retorna os detalhes do orçamento atualizado.
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Método HTTP DELETE para excluir um orçamento específico.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            pk: O ID do orçamento a ser obtido.

        Retorna:
            Response: Uma resposta HTTP com status 204 No Content como
            confirmação.
        """

        # Obtém o orçamento específico com base no ID fornecido.
        budget = self.get_budget(pk)

        # Remove o orçamento do banco de dados.
        budget.delete()

        # Retorna uma resposta vazia com status 204 No Content como
        # confirmação.
        return Response(status=status.HTTP_204_NO_CONTENT)

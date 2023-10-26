from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from finances.models import Account, Category, Transaction, Budget
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Account.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        validate: Valida os dados fornecidos durante a serialização.

    Campos:
        Todos os campoos do modelo Account.
    """
    class Meta:
        model = Account
        fields = '__all__'

    def validate(self, data):
        """
        Validação personalizada para o serializer Account.

        Parâmetros:
            data: Os dados a serem validados.

        Retorna:
            data: Os dados validados.
        """

        if data.get('balance') is not None and data['balance'] < 0:
            raise serializers.ValidationError(
                {'balance': ['The balance must not be negative.']}
            )

        request = self.context.get('request')
        if request and request.method == 'PATCH':
            if 'balance' in data:
                instance = self.instance
                balance_update = data['balance']
                instance.balance = balance_update

                instance.save()

                return {'balance': instance.balance}

        if not data.get('owner'):
            raise serializers.ValidationError(
                {'owner': ['Este campo é obrigatório.']}
            )

        return data


class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Budget.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        validate: Valida os dados fornecidos durante a serialização.

    Campos:
        Todos os campos do modelo Budget.
    """

    class Meta:
        model = Budget
        fields = '__all__'

    def validate(self, data):
        """
        Validação personalizada para o serializer Account.

        Parâmetros:
            data: Os dados a serem validados.

        Retorna:
            data: Os dados validados.
        """

        if not data.get('account'):
            raise serializers.ValidationError(
                {'account': ['Este campo é obrigatório.']}
            )
        if not data.get('category'):
            raise serializers.ValidationError(
                {'category': ['Este campo é obrigatório.']}
            )
        if not data.get('amount'):
            raise serializers.ValidationError(
                {'amount': ['Este campo é obrigatório.']}
            )

        existing_budgets = Budget.objects.filter(
            account=data.get('account'),
            category=data.get('category'),
            amount=data.get('amount'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )

        if existing_budgets.exists():
            raise serializers.ValidationError('The budget already exists.')

        return data

    def update(self, instance, validated_data):
        """
        Atualiza uma transação existente e ajusta o gasto do orçamento, se
        necessário.

        Parâmetros:
            instance: A transação existente.
            validated_data: Dados validados para atualização.

        Retorna:
            Transaction: A transação atualizada.
        """

        request = self.context.get('request')
        if request and request.method == 'PUT':
            if 'amount' in validated_data:
                budget_amount = validated_data['amount']
                instance.amount = budget_amount

                if budget_amount < 0:
                    raise serializers.ValidationError(
                        {'amount': [
                            'The budget value must not be negative.'
                        ]
                        }
                    )

                instance.save()
                return instance

        instance.amount = validated_data.get('amount', instance.amount)
        instance.account = validated_data.get('account', instance.account)
        instance.category = validated_data.get('category', instance.category)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date
        )
        instance.end_date = validated_data.get('end_date', instance.end_date)

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Category.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        Nenhum método específico nesta classe.

    Campos:
        Todos os campos do modelo Category.
    """
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, data):
        existing_category = Category.objects.filter(
            name=data.get('name')
        )

        if existing_category.exists():
            raise serializers.ValidationError('The category already exists.')

        return data


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Transaction.

    Campos:
        - id: O identificador único da transação (somente leitura).
        - amount: O valor da transação.
        - description: A descrição da transação.
        - account: A conta associada à transação.
        - category: A categoria à qual a transação pertence.

    Métodos:
        - validate: Realiza validações personalizadas durante a serialização.
        - create: Cria uma nova instância de transação e atualiza os saldos da
        conta e orçamento, se aplicável.
        - update: Atualiza uma transação existente e ajusta o gasto do
        orçamento, se necessário.
    """
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'description', 'account', 'category')

    def validate(self, data):
        """
        Valida os dados fornecidos durante a serialização.

        Parâmetros:
            data: Os dados a serem validados.

        Retorna:
            data: Os dados validados.
        """

        if not data.get('amount'):
            raise serializers.ValidationError(
                {'amount': ['Este campo é obrigatório.']}
            )

        if not data.get('description'):
            raise serializers.ValidationError(
                {'description': ['Este campo é obrigatório.']}
            )

        if not data.get('account'):
            raise serializers.ValidationError(
                {'account': ['Este campo é obrigatório.']}
            )

        if not data.get('category'):
            raise serializers.ValidationError(
                {'category': ['Este campo é obrigatório.']}
            )

        account = data['account']
        if data.get('amount') > account.balance:
            raise serializers.ValidationError(
                'Insufficient balance for the transaction.'
            )

        category = data['category']

        if category.budget_set.exists():
            budget = category.budget_set.first()
            if data.get('amount') > budget.amount:
                raise serializers.ValidationError(
                    'The value of the transaction exceeds the budget for this category.'  # noqa: 501
                )

        return data

    def create(self, validated_data):
        """
        Cria uma nova transação e atualiza o saldo da conta e o gasto do
        orçamento, se aplicável.

        Parâmetros:
            validated_data: Dados validados da transação.

        Retorna:
            transaction: A transação recém-criada.
        """

        transaction_amount = validated_data['amount']
        account = validated_data['account']
        category = validated_data['category']
        budget = None

        if category.budget_set.exists():
            budget = category.budget_set.first()

        transaction = Transaction.objects.create(**validated_data)

        account.balance -= transaction_amount
        account.save()

        if budget:
            budget.spent += transaction_amount
            budget.save()

        return transaction

    def update(self, instance, validated_data):
        """
        Atualiza uma transação existente e ajusta o gasto do orçamento, se
        necessário.

        Parâmetros:
            instance: A transação existente.
            validated_data: Dados validados para atualização.

        Retorna:
            transaction: A transação atualizada.
        """

        old_amount = instance.amount
        new_amount = validated_data.get('amount', old_amount)
        account = instance.account
        category = instance.category

        if category.budget_set.exists():
            budget = category.budget_set.first()
            if new_amount != old_amount:
                difference = new_amount - old_amount
                budget.spent += difference
                budget.save()

        instance.amount = new_amount
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        account.save()

        return instance


class OwnerSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Owner.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        validate: Valida os dados fornecidos durante a serialização.
        create: Cria uma nova instância de Owner.

    Campos:
        - id
        - username
        - first_name
        - last_name
        - email
        - password
    """
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Validação personalizada para o serializer Onwer.

        Parâmetros:
            data: os dados a serem validados.

        Retorna:
            data: Os dados validados.
        """

        is_creation_request = self.context.get('is_creation_request', False)

        if is_creation_request:
            if not data.get('first_name'):
                raise serializers.ValidationError(
                    {'first_name': ['Este campo é obrigatório.']}
                )
            if not data.get('last_name'):
                raise serializers.ValidationError(
                    {'last_name': ['Este campo é obrigatório.']}
                )
            if not data.get('email'):
                raise serializers.ValidationError(
                    {'email': ['Este campo é obrigatório.']}
                )

        if 'password' in data:
            data['password'] = make_password(data['password'])

        return data

    def create(self, validated_data):
        """
        Cria uma nova instância de Owner.

        Parâmetros:
            validated_data: Os dados validados para criar o proprietário.

        Retorna:
            user: A instância de Owner criada.
        """

        owner = User.objects.create(**validated_data)

        return owner

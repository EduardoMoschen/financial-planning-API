from rest_framework import serializers
from finances.models import Account, Category, Transaction, Budget
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'description', 'account', 'category')

    def validate(self, data):
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
                'Insufficient balance to carry out the transaction.')

        return data

    def create(self, validated_data):
        transation_amount = validated_data['amount']
        account = validated_data['account']

        transaction = Transaction.objects.create(**validated_data)

        account.balance -= transation_amount
        account.save()

        return transaction

    def update(self, instance, validated_data):
        old_amount = instance.amount
        new_amount = validated_data.get('amount', old_amount)
        account = instance.account

        if new_amount > old_amount:
            difference = new_amount - old_amount
            if account.balance >= difference:
                account.balance -= difference
            else:
                raise serializers.ValidationError(
                    'Insufficient balance to carry out the transaction.'
                )
        elif new_amount < old_amount:
            refund_amount = old_amount - new_amount
            account.balance += refund_amount

        instance.amount = new_amount
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.category = validated_data.get('cateogry', instance.category)
        instance.save()
        account.save()

        return instance


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'password'
        )
        # extra_kwargs pode ser usada para fornecer argumentos adicionais.
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        owner = User.objects.create(
            username=validated_data['username'],
            # Caso não seja fornecido o fn e ln, será uma string vazia.
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            password=validated_data['password']
        )

        return owner

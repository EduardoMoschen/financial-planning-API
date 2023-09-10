from rest_framework import serializers
from finances.models import Account, Category, Transaction, Budget
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            if 'balance' in data:
                instance = self.instance
                balance_update = data['balance']
                instance.balance = balance_update

                if instance.balance < 0:
                    raise serializers.ValidationError(
                        {'balance': ['The balance must not be negative.']}
                    )

                instance.save()

                return {'balance': instance.balance}

        if not data.get('owner'):
            raise serializers.ValidationError(
                {'owner': ['Este campo é obrigatório.']}
            )

        return data


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

    def validate(self, data):
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
        if not data.get('start_date'):
            return serializers.ValidationError(
                {'start_date': ['Este campo é obrigatório.']}
            )
        if not data.get('end_date'):
            return serializers.ValidationError(
                {'end_date': ['Este campo é obrigatório.']}
            )

        return data


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

        category = data['category']
        if category.budget_set.exists() and \
                data.get('amount') > category.budget_set.first().amount:
            raise serializers.ValidationError(
                'Transaction amount exceeds the budget for this category.'
            )
        return data

    def create(self, validated_data):
        transation_amount = validated_data['amount']
        account = validated_data['account']
        category = validated_data['category']

        if category.budget and transation_amount > category.budget.amount:
            return serializers.ValidationError(
                'Transaction amount exceeds the budget for this category.'
            )

        transaction = Transaction.objects.create(**validated_data)

        account.balance -= transation_amount
        account.save()

        if category.budget:
            category.budget.spent += transation_amount
            category.budget.save()

        return transaction

    def update(self, instance, validated_data):
        old_amount = instance.amount
        new_amount = validated_data.get('amount', old_amount)
        account = instance.account
        category = instance.category

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

        if category.budget:
            category.budget.spent -= old_amount
            category.budget.spent += new_amount
            category.budget.save()

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

    def validate(self, data):
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

        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'This email is already in use.'
            )
        return value

    def create(self, validated_data):
        owner = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data['email'],
            password=validated_data['password']
        )

        return owner

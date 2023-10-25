from django.contrib.auth.models import User
from django.test import TestCase

from finances.serializers import OwnerSerializer


class OwnerSerializerTestCase(TestCase):
    """
    Testes para o serializador de Proprietário.

    Esta classe contém testes para o serializador de Owner, que é responsável
    por validar e transformar dados de usuários em um formato adequado para o
    uso na API.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria instâncias
        iniciais de dados necessários para os testes.
        """

        self.valid_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@test.com',
            'password': 'testpassword'
        }

        self.invalid_data_missing_first_name = {
            'username': 'testuser',
            'last_name': 'Doe',
            'email': 'test@test.com',
            'password': 'testpassword'
        }

        self.invalid_data_missing_last_name = {
            'username': 'testuser',
            'first_name': 'John',
            'email': 'test@test.com',
            'password': 'testpassword'
        }

        self.invalid_data_missing_email = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword'
        }

    def test_validate_method(self):
        """
        Testa o método de validação.

        Este teste verifica se o método de validação do serializador funciona
        corretamente ao validar os dados do usuário.
        """

        serializer = OwnerSerializer(
            data=self.valid_data,
            context={'is_creation_request': True}
        )

        self.assertTrue(serializer.is_valid())

        serializer = OwnerSerializer(
            data=self.invalid_data_missing_first_name,
            context={'is_creation_request': True}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)

        serializer = OwnerSerializer(
            data=self.invalid_data_missing_last_name,
            context={'is_creation_request': True}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('last_name', serializer.errors)

        serializer = OwnerSerializer(
            data=self.invalid_data_missing_email,
            context={'is_creation_request': True}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_create_method(self):
        """
        Testa o método de criação.

        Este teste verifica se o método de criação do serializador cria
        corretamente uma nova instância de usuário com os dados fornecidos.
        """

        serializer = OwnerSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user_instance = serializer.save()

        self.assertIsInstance(user_instance, User)
        self.assertEqual(user_instance.username, 'testuser')
        self.assertEqual(user_instance.first_name, 'John')
        self.assertEqual(user_instance.last_name, 'Doe')
        self.assertEqual(user_instance.email, 'test@test.com')
        self.assertTrue(user_instance.check_password('testpassword'))

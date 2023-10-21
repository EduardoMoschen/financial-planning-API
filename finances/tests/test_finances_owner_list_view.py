from django.test import TestCase
from django.contrib.auth.models import User
from finances.serializers import OwnerSerializer
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class OwnerAPIListTest(TestCase):
    """
    Testes para a API de OwnerAPIList.

    Esta classe contém testes para os métodos da API de OwnerAPIList, que lida
    com operações relacionadas aos titulares das contas bancárias.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria instâncias
        iniciais de objetos necessários para os testes.
        """

        self.user1 = User.objects.create_user(
            username='user1',
            password='password1',
            first_name='Carlos',
            last_name='Alberto',
            email='carlos@email.com'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            password='password2',
            first_name='Gustavo',
            last_name='Barreto',
            email='gustavo@email.com'
        )

        self.client = APIClient()

    def test_get_owners(self):
        """
        Testa o método GET para obter todos os titulares cadastrados.

        Este teste verifica se o método GET retorna todos os titulares com o
        status HTTP 200 OK.
        """

        response = self.client.get('/api/owners/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        owners = User.objects.all()
        serializer = OwnerSerializer(owners, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_no_owners(self):
        """
        Testa o método GET quando não há titulares cadastrados.

        Este teste verifica se o método GET retorna a mensagem apropriada
        quando não há titulares cadastrados.
        """

        User.objects.all().delete()

        response = self.client.get('/api/owners/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'message': 'There are no registered owners.'}
        )

    def test_create_owner(self):
        """
        Testa o método POST para criar um novo titular.

        Este teste verifica se o método POST cria um novo titular corretamente
        e retorna o status HTTP 201 CREATED.
        """

        new_owner_data = {
            'username': 'username3',
            'password': 'password3',
            'first_name': 'Arthur',
            'last_name': 'Passos',
            'email': 'arthur@email.com'
        }

        response = self.client.post(
            '/api/owners/',
            data=new_owner_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_owner = User.objects.get(username=new_owner_data['username'])

        self.assertEqual(created_owner.username, new_owner_data['username'])
        self.assertEqual(
            created_owner.first_name,
            new_owner_data['first_name']
        )
        self.assertEqual(created_owner.last_name, new_owner_data['last_name'])
        self.assertEqual(created_owner.email, new_owner_data['email'])

        serializer = OwnerSerializer(created_owner)
        self.assertEqual(response.data, serializer.data)

    def test_create_owner_invalid_data(self):
        """
        Testa o método POST para criar um novo titular com dados inválidos.

        Este teste verifica se o método POST cria um novo titular com os dados
        passados de forma inválida e retorna o status HTTP 400 BAD REQUEST.
        """

        url = reverse('owners_list')

        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from django.test import TestCase
from finances.models import Category
from finances.serializers import CategorySerializer
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class CategoryAPIListTest(TestCase):
    """
    Testes para a API de CategoryAPIList.

    Esta classe contém testes para os métodos da API de CategoryAPIList, que
    lida com operações relacionadas às categorias que serão usadas nas
    transações e orçamentos.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria instâncias
        iniciais de objetos necessários para os testes.
        """

        self.category_1 = Category.objects.create(
            name='Alimentação'
        )

        self.category_2 = Category.objects.create(
            name='Academia'
        )

        self.user = User.objects.create_user(
            username='user1',
            password='password1',
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_categories(self):
        """
        Testa o método GET para obter todas as categorias cadastradas.

        Este teste verifica se o método GET retorna todas as categorias com o
        status HTTP 200 OK.
        """

        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_no_categories(self):
        """
        Testa o método GET quando não há categorias cadastradas.

        Este teste verifica se o método GET retorna a mensagem apropriada
        quando não há categorias registradas.
        """

        Category.objects.all().delete()

        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'message': 'There are no registered categories.'}
        )

    def test_create_category(self):
        """
        Testa o método POST para criar uma nova conta.

        Este teste verifica se o método POST cria uma nova categoria
        corretamente e retorna o status HTTP 201 CREATED.
        """

        new_category_data = {
            'name': 'Medicamentos'
        }

        response = self.client.post(
            '/api/categories/',
            data=new_category_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(name=new_category_data['name'])
        self.assertEqual(created_category.name, new_category_data['name'])

        serializer = CategorySerializer(created_category)
        self.assertEqual(response.data, serializer.data)

    def test_create_category_with_invalid_data(self):
        """
        Testa o método POST para criar uma nova categoria com dados inválidos.

        Este teste verifica se o método POST cria uma nova categoria com os
        dados passados de forma inválida e retorna o status HTTP 400 BAD
        REQUEST.
        """

        new_category_data = {
            'name': ''
        }

        response = self.client.post(
            '/api/categories/',
            data=new_category_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

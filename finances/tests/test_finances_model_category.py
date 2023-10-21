from django.test import TestCase
from finances.models import Category


class CategoryModelTestCase(TestCase):
    """
    Teste para o modelo Category.

    Esta classe contém teste para o modelo Category, que representa uma
    categoria de uma transação financeira.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Este método é executado antes de cada teste. Ele cria as instâncias
        iniciais de objetos necessárias para os testes.
        """

        self.category = Category.objects.create(name='Food')

    def test_category_str_with_expected_output(self):
        """
        Testa o método __str__() do modelo Category.

        Este teste verifica se o método __str__() do modelo Category retorna a
        saída esperada, que inclui o nome da categoria.
        """

        expected_output = f'Category: {self.category.name}'
        self.assertEqual(str(self.category), expected_output)

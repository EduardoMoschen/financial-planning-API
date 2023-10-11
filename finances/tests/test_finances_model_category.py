from django.test import TestCase
from finances.models import Category


class CategoryModelTestCase(TestCase):
    """
    Teste para o modelo Category.

    Esta classe contém teste para o modelo Category, que representa uma
    categoria de uma transação financeira.
    """

    def test_category_str_with_expected_output(self):
        """
        Testa o método __str__() do modelo Category.

        Este teste verifica se o método __str__() do modelo Category retorna a
        saída esperada, que inclui o nome da categoria.

        Casos de Teste:
            - Cria uma categoria.
            - Compara a representaçao da string da categoria com a saída
            esperada.

        Notas:
            - Deve se certificar de ter criado instâncias de objetos
            relacionados para garantir a integridade do teste.
        """

        category = Category.objects.create(name="Food")

        expected_output = f'Category: {category.name}'

        self.assertEqual(str(category), expected_output)

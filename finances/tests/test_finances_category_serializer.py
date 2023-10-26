from django.test import TestCase
from finances.serializers import CategorySerializer
from finances.models import Category


class CategorySerializerTestCase(TestCase):
    """
    Testes para o serializador de Categoria.

    Esta classe contém testes para o serializador de Categoria, que é
    responsável por validar e transformar os dados das categorias em um formato
    adequado para uso na API.
    """

    def test_validate_unique_category(self):
        """
        Testa se a validação impede a criação de categorias duplicadas.

        Este teste verifica se a validação personalizada impede a criação de
        categorias duplicadas e lança uma exceção de validação se uma categoria
        com o mesmo nome já existir.
        """

        Category.objects.create(name='Category1')

        category_data = {
            'name': 'Category1'
        }

        serializer = CategorySerializer(data=category_data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            'The category already exists.',
            serializer.errors['non_field_errors']
        )

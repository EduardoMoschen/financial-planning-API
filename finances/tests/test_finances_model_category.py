from django.test import TestCase
from finances.models import Category


class CategoryModelTestCase(TestCase):
    def test_category_str_with_expected_output(self):
        category = Category.objects.create(name="Food")

        expected_output = f'Category: {category.name}'

        self.assertEqual(str(category), expected_output)

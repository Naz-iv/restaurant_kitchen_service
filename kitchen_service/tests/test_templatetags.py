from django.test import TestCase

from kitchen_service.models import Ingredient
from kitchen_service.templatetags.get_length import get_length


class GetLengthFilterTests(TestCase):

    def test_get_length_for_list(self):
        result = get_length([1, 2, 3])
        self.assertEqual(result, 3)

    def test_get_length_for_queryset(self):
        Ingredient.objects.create(name="beckon")
        Ingredient.objects.create(name="milk")
        Ingredient.objects.create(name="suger")
        Ingredient.objects.create(name="water")

        self.assertEqual(get_length(Ingredient.objects.all()), 4)


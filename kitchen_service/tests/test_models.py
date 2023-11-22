from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen_service.models import Ingredient, DishType, Dish, Unit


class ModelsTests(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            name="test ingredient"
        )
        self.unit = Unit.objects.create(
            name="unit"
        )

        self.type = DishType.objects.create(
            name="test type"
        )
        self.cook = get_user_model().objects.create(
            username="Test cook1",
            first_name="Test",
            last_name="Cook1",
            years_of_experience=10
        )
        self.cook2 = get_user_model().objects.create(
            username="Test cook2",
            first_name="Test",
            last_name="Cook2",
            years_of_experience=2
        )
        self.dish = Dish.objects.create(
            name="test dish",
            description="test dish description",
            price=10,
            dish_type=self.type,
        )
        self.dish.cook.set([self.cook, self.cook2])

    def test_ingredient_str(self):
        self.assertEquals(str(self.ingredient), self.ingredient.name)

    def test_unit_str(self):
        self.assertEquals(str(self.unit), self.unit.name)

    def test_dish_type_str(self):
        self.assertEquals(str(self.type), self.type.name)

    def test_cook_str(self):
        self.assertEquals(
            str(self.cook),
            f"{self.cook.username} ({self.cook.first_name} "
            f"{self.cook.last_name})"
        )

    def test_dish_str(self):
        self.assertEquals(
            str(self.dish),
            self.dish.name
        )

    def test_cook_ordering(self):
        self.assertEquals(
            list(get_user_model().objects.all()),
            [self.cook, self.cook2]
        )

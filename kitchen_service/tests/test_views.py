from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen_service.forms import HomeSearchForm
from kitchen_service.models import DishType, Dish, Ingredient, Cook

HOME_URL = reverse("kitchen_service:home")
DISH_TYPE_LIST_URL = reverse("kitchen_service:dish-type-list")
DISH_LIST_URL = reverse("kitchen_service:dish-list")
COOK_LIST_URL = reverse("kitchen_service:cook-list")
INGREDIENT_LIST_URL = reverse("kitchen_service:ingredient-list")
URLS = [
    HOME_URL,
    DISH_TYPE_LIST_URL,
    DISH_LIST_URL,
    COOK_LIST_URL,
    INGREDIENT_LIST_URL,
    reverse("kitchen_service:dish-create"),
    reverse("kitchen_service:dish-detail", kwargs={"pk": 1}),
    reverse("kitchen_service:dish-update", kwargs={"pk": 1}),
    reverse("kitchen_service:cook-create"),
    reverse("kitchen_service:cook-detail", kwargs={"pk": 1}),
    reverse("kitchen_service:dish-type-list"),
    reverse("kitchen_service:dish-type-update", kwargs={"pk": 1}),
    reverse("kitchen_service:dish-type-detail", kwargs={"pk": 1}),
    reverse("kitchen_service:ingredient-create"),
    reverse("kitchen_service:ingredient-detail", kwargs={"pk": 1}),
    reverse("kitchen_service:ingredient-update", kwargs={"pk": 1}),
]


class PublicTest(TestCase):

    def test_login_required_to_all_pages(self) -> None:
        for url in URLS:
            with self.subTest(url):
                response = self.client.get(url)

                self.assertNotEqual(response.status_code, 200)


class PrivateTest(TestCase):

    def test_access_with_login(self) -> None:
        user = get_user_model().objects.create(
            username="test",
            years_of_experience=2,
            password="test_password",
        )
        self.client.force_login(user)
        dish_type = DishType.objects.create(id=1, name="test")
        Ingredient.objects.create(id=1, name="test")
        Dish.objects.create(
            name="test",
            description="test_description",
            price=10.5,
            dish_type=dish_type,
        )
        for url in URLS:
            with self.subTest(url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)


class DishListTest(TestCase):

    def test_search_filter_working(self) -> None:
        user = get_user_model().objects.create(
            username="test",
            years_of_experience=2,
            password="test_password",
        )
        self.client.force_login(user)
        dish_type = DishType.objects.create(name="test")

        for dish_index in range(1, 12):
            Dish.objects.create(
                name=f"test dish №{dish_index}",
                description="test_description",
                price=10.5,
                dish_type=dish_type,
            )

        response = self.client.get(DISH_LIST_URL + "?name=1")
        self.assertEqual(response.context["dish_list"].count(), 3)


class IngredientListTest(TestCase):

    def test_ingredient_search_filter_working(self) -> None:
        user = get_user_model().objects.create(
            username="test",
            years_of_experience=2,
            password="test_password",
        )
        self.client.force_login(user)

        dish_type = DishType.objects.create(name="test")
        Dish.objects.create(
            name=f"test dish",
            description="test_description",
            price=10.5,
            dish_type=dish_type,
        )
        for index in range(1, 12):
            Ingredient.objects.create(
                name=f"test ingredient №{index}",
            )

        response = self.client.get(INGREDIENT_LIST_URL + "?name=1")
        self.assertEqual(response.context["ingredient_list"].count(), 3)


class CookListTest(TestCase):

    def test_cook_search_filter_working(self) -> None:
        user = get_user_model().objects.create(
            username="Main user",
            years_of_experience=2,
            password="test_password",
        )
        self.client.force_login(user)

        dish_type = DishType.objects.create(name="test")
        Dish.objects.create(
            name=f"test dish",
            description="test_description",
            price=10.5,
            dish_type=dish_type,
        )
        for index in range(1, 12):
            get_user_model().objects.create(
                username=f"test user {index}",
                years_of_experience=2,
                password="test_password",
            )

        response = self.client.get(COOK_LIST_URL + "?name=1")
        self.assertEqual(response.context["cook_list"].count(), 3)


class DishTypeListTest(TestCase):

    def test_dish_type_search_filter_working(self) -> None:
        user = get_user_model().objects.create(
            username="test",
            years_of_experience=2,
            password="test_password",
        )
        self.client.force_login(user)

        dish_type = DishType.objects.create(name="main")
        Dish.objects.create(
            name=f"test dish",
            description="test_description",
            price=10.5,
            dish_type=dish_type,
        )
        for index in range(1, 12):
            DishType.objects.create(
                name=f"test dish type №{index}",
            )

        response = self.client.get(DISH_TYPE_LIST_URL + "?name=1")
        self.assertEqual(response.context["dishtype_list"].count(), 3)


class HomePageTest(TestCase):
    def test_global_search_filter_working(self) -> None:
        user = get_user_model().objects.create(
            username="test",
            years_of_experience=2,
            password="test_password",
        )
        self.client.force_login(user)

        dish_type = DishType.objects.create(name="test")
        Dish.objects.create(
            name=f"test dish",
            description="test_description",
            price=10.5,
            dish_type=dish_type,
        )
        Ingredient.objects.create(name="test")

        for index in range(1, 12):
            DishType.objects.create(
                name=f"Dish type №{index}",
            )
            Ingredient.objects.create(
                name=f"Ingredient №{index}"
            )
            Dish.objects.create(
                name=f"Dish №{index}",
                description="description",
                price=10.5,
                dish_type=dish_type,
            )
        form_data = {"search_input": "test"}

        response = self.client.post(HOME_URL, data=form_data)

        self.assertEqual(response.context["cook_search"].count(), 1)
        self.assertEqual(response.context["dish_search"].count(), 1)
        self.assertEqual(response.context["ingredient_search"].count(), 1)
        self.assertEqual(response.context["dishtype_search"].count(), 1)

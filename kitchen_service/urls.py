from django.urls import path
from kitchen_service.views import (
    index,
    DishListView,
    CookListView,
    IngredientListView,
    DishDetailView,
    CookDetailView,
    IngredientDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    IngredientDeleteView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    IngredientCreateView,
    IngredientUpdateView,
    DishTypeListView,
    DishTypeDetailView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    DishTypeCreateView
)


urlpatterns = [
    path("", index, name="home"),

    path("dishes/",
         DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/",
         DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/",
         DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/",
         DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/",
         DishDeleteView.as_view(), name="dish-delete"),

    path("cooks/",
         CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/",
         CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create/",
         CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/update/",
         CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/delete/",
         CookDeleteView.as_view(), name="cook-delete"),

    path("ingredients/",
         IngredientListView.as_view(), name="ingredient-list"),
    path("ingredients/<int:pk>/",
         IngredientDetailView.as_view(), name="ingredient-detail"),
    path("ingredients/create/",
         IngredientCreateView.as_view(), name="ingredient-create"),
    path("ingredients/<int:pk>/update/",
         IngredientUpdateView.as_view(), name="ingredient-update"),
    path("ingredients/<int:pk>/delete/",
         IngredientDeleteView.as_view(), name="ingredient-delete"),

    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/<int:pk>/",
         DishTypeDetailView.as_view(), name="dish-type-detail"),
    path("dish-types/<int:pk>/update/",
         DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-types/<int:pk>/delete/",
         DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dish-types/create/",
         DishTypeCreateView.as_view(), name="dish-type-create"),
]

app_name = "kitchen_service"

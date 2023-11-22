from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from kitchen_service.models import Dish, Ingredient, DishType


@login_required(login_url="/login/")
def index(request):
    context = {
        'segment': 'index',
        "featured_cook": get_user_model().objects.order_by("-years_of_experience")[0],
        "dish_type_count": DishType.objects.distinct().count(),
        "dish_count": Dish.objects.distinct().count(),
        "most_expensive_dish": Dish.objects.order_by("-price")[0]
    }
    print("running index function")
    return render(request, "index.html", context)


class DishListView(ListView):
    model = Dish


class DishDetailView(DetailView):
    model = Dish


class DishCreateView(CreateView):
    model = Dish


class DishUpdateView(UpdateView):
    model = Dish


class DishDeleteView(DeleteView):
    success_url = reverse_lazy("kitchen_service:dish_list")


class CookListView(ListView):
    model = get_user_model()


class CookDetailView(DetailView):
    model = get_user_model()
    template_name = "kitchen_service/cook_detail.html"


class CookCreateView(CreateView):
    model = get_user_model()


class CookUpdateView(UpdateView):
    model = get_user_model()


class CookDeleteView(DeleteView):
    success_url = reverse_lazy("kitchen_service:cook_list")


class IngredientListView(ListView):
    model = Ingredient


class IngredientDetailView(DetailView):
    model = Ingredient


class IngredientCreateView(CreateView):
    model = Ingredient


class IngredientUpdateView(UpdateView):
    model = Ingredient


class IngredientDeleteView(DeleteView):
    success_url = reverse_lazy("kitchen_service:dish_list")

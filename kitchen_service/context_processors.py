from django.contrib.auth import get_user_model
from django.http import HttpRequest

from kitchen_service.models import DishType, Dish


def stats_context_processor(request:HttpRequest) -> dict:

    stat_data = {
        "dish_type_count": DishType.objects.distinct().count(),
        "dish_count": Dish.objects.distinct().count(),
    }

    cooks = get_user_model().objects.order_by("-years_of_experience")
    dishes = Dish.objects.order_by("-price")
    if cooks:
        stat_data["featured_cook"] = cooks[0]

    if dishes:
        stat_data["dishes"] = dishes[0]

    return {"stat_data": stat_data}

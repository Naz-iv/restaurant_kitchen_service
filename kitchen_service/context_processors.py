from django.contrib.auth import get_user_model
from django.http import HttpRequest

from kitchen_service.models import DishType, Dish


def stats_context_processor(request:HttpRequest) -> dict:
    stat_data = {
        "featured_cook": get_user_model().objects.order_by("-years_of_experience")[0],
        "dish_type_count": DishType.objects.distinct().count(),
        "dish_count": Dish.objects.distinct().count(),
        "most_expensive_dish": Dish.objects.order_by("-price")[0]
    }
    return {"stat_data": stat_data}

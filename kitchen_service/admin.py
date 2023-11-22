from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from kitchen_service.models import (
    Ingredient,
    Unit,
    DishType,
    Cook,
    Dish,
    DishIngredient
)

admin.site.unregister(Group)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience",)}),)
    )
    list_filter = UserAdmin.list_filter + ("years_of_experience",)
    ordering = ("-years_of_experience",)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("dish_type", "price", "description")
    list_filter = ("dish_type", "price")
    search_fields = ("dish__name",)


@admin.register(DishIngredient)
class DishIngredientAdmin(admin.ModelAdmin):
    list_display = ("dish", "ingredient", "quantity", "unit")
    list_filter = ("dish", "ingredient")
    search_fields = ("dish__name",)

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from core.settings import AUTH_USER_MODEL


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Unit(models.Model):
    name = models.CharField(
        max_length=255,
        choices={
            ("kilograms", "kilograms"),
            ("grams", "grams"),
            ("milligrams", "milligrams"),
            ("liter", "liter"),
            ("milliliter", "milliliter"),
            ("tea spoon", "tea spoon"),
            ("kitchen spoon", "kitchen spoon"),
            ("unit", "unit")
        },
        default="unit"
    )

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "dish type"
        verbose_name_plural = "dish types"
        ordering = ('name',)


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    class Meta:
        ordering = ["-years_of_experience"]


class DishIngredient(models.Model):
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE,
                             related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name="dishes")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        verbose_name = "dish ingredient"
        verbose_name_plural = "dish ingredients"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                validators=[MinValueValidator(0.0)])
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cook = models.ManyToManyField(AUTH_USER_MODEL, related_name="dishes")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "dishes"
        ordering = ("name",)

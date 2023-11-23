from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from kitchen_service.models import Dish, Cook, DishType, DishIngredient


class CookCreateForm(UserCreationForm):
    dish = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
            "dish",
        )


class CookUpdateForm(CookCreateForm):

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "years_of_experience", "dish",]


class DishTypeForm(forms.ModelForm):
    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = DishType
        fields = "__all__"


class DishForm(forms.ModelForm):
    cook = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'dish_type', 'cook']


DishIngredientFormSet = inlineformset_factory(
    Dish,
    DishIngredient,
    fields=('ingredient', 'unit', 'quantity'),
    extra=6,
    can_delete=True,
)


class HomeSearchForm(forms.Form):
    search_input = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            {"placeholder": "Search by name"}
        )
    )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            {"placeholder": "Search by username"}
        )
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            {"placeholder": "Search by name"}
        )
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            {"placeholder": "Search by name"}
        )
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            {"placeholder": "Search by name"}
        )
    )

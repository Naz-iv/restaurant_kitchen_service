from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from kitchen_service.forms import (
    DishForm,
    CookCreateForm,
    CookUpdateForm,
    DishTypeForm,
    DishIngredientFormSet,
    HomeSearchForm,
    CookSearchForm,
    IngredientSearchForm,
    DishTypeSearchForm,
    DishSearchForm
)
from kitchen_service.models import Dish, Ingredient, DishType


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    search_input = ""

    if request.method == "POST":
        form = HomeSearchForm(request.POST)
        if form.is_valid():
            search_input = form.cleaned_data["search_input"]
    else:
        form = HomeSearchForm()

    context = {
        "form": form
    }

    if search_input:
        cook_search = get_user_model().objects.filter(
            Q(username__icontains=search_input)
            | Q(first_name__icontains=search_input)
            | Q(last_name__icontains=search_input)
        )
        dish_search = Dish.objects.filter(name__icontains=search_input)
        ingredient_search = Ingredient.objects.filter(name__icontains=search_input)
        dishtype_search = DishType.objects.filter(name__icontains=search_input)

        context["cook_search"] = cook_search
        context["dish_search"] = dish_search
        context["ingredient_search"] = ingredient_search
        context["dishtype_search"] = dishtype_search
        context["search_input"] = search_input

    return render(request, "index.html", context=context)


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    paginate_by = 6

    def get_queryset(self):
        name = self.request.GET.get("name")
        queryset = Dish.objects.all()

        if name:
            return queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = DishSearchForm(initial={
            "name": name
        })
        return context


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    queryset = Dish.objects.prefetch_related("ingredients__ingredient", "ingredients__unit", "cook")


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen_service:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DishIngredientFormSet(self.request.POST)
        else:
            context['formset'] = DishIngredientFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen_service:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DishIngredientFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DishIngredientFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen_service:dish-list")


class CookListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    paginate_by = 6

    def get_queryset(self):
        username = self.request.GET.get("username")
        queryset = get_user_model().objects.all()

        if username:
            return queryset.filter(
                username__icontains=username
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")

        context["search_form"] = CookSearchForm(initial={
            "username": username
        })
        return context


class CookDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "kitchen_service/cook_detail.html"
    queryset = get_user_model().objects.prefetch_related("dishes", "dishes__dish_type")


class CookCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    form_class = CookCreateForm
    success_url = reverse_lazy("kitchen_service:cook-list")


class CookUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen_service:cook-list")


class CookDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("kitchen_service:cook-list")


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    paginate_by = 6

    def get_queryset(self):
        name = self.request.GET.get("name")
        queryset = Ingredient.objects.all()

        if name:
            return queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = IngredientSearchForm(initial={
            "name": name
        })
        return context


class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    queryset = Ingredient.objects.prefetch_related("dishes__dish")


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen_service:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen_service:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen_service:ingredient-list")


class DishTypeListView(LoginRequiredMixin, ListView):
    model = DishType
    paginate_by = 6

    def get_queryset(self):
        name = self.request.GET.get("name")
        queryset = DishType.objects.prefetch_related("dishes")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = DishTypeSearchForm(initial={
            "name": name
        })
        return context


class DishTypeDetailView(LoginRequiredMixin, DetailView):
    model = DishType
    queryset = DishType.objects.prefetch_related("dishes")


class DishTypeCreateView(LoginRequiredMixin, CreateView):
    model = DishType
    form_class = DishTypeForm
    success_url = reverse_lazy("kitchen_service:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DishType
    form_class = DishTypeForm
    success_url = reverse_lazy("kitchen_service:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen_service:dish-type-list")

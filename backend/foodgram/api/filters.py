from django_filters.rest_framework import FilterSet, filters
from django_filters import AllValuesMultipleFilter

from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug',
                                   lookup_expr='isnull')
    is_favorited = filters.BooleanFilter(method="is_favorited_filter")
    is_in_shopping_cart = filters.BooleanFilter(method="is_in_shopping_cart_filter")

    class Meta:
        model = Recipe
        fields = ("tags",)

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(recipe_fav__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(recipe_basket__user=user)
        return queryset

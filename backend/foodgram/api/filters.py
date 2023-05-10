from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(FilterSet):
    is_favorited = filters.BooleanFilter(method='check_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='check_in_shopping_cart')
    author = filters.CharFilter(method='is_author')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def check_favorited(self, queryset, field_name, value):
        if value:
            return queryset.filter(favourites__user=self.request.user)
        return queryset

    def check_in_shopping_cart(self, queryset, field_name, value):
        if value:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset

    def is_author(self, queryset, field_name, value):
        if value:
            author = get_object_or_404(
                User,
                id=value
            )
            return queryset.filter(author=author)
        return queryset

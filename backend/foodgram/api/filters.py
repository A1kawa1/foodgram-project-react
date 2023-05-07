from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(FilterSet):
    is_favorited = filters.BooleanFilter(method='check_favorited')
    tags = filters.CharFilter(method='on_tags')
    author = filters.CharFilter(method='is_author')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'tags')

    def check_favorited(self, queryset, field_name, value):
        if value:
            return queryset.filter(favourites__user=self.request.user)
        return queryset

    def on_tags(self, queryset, field_name, value):
        if value:
            return queryset.filter(tags__slug=value)
        return queryset

    def is_author(self, queryset, field_name, value):
        if value:
            author = get_object_or_404(
                User,
                id=value
            )
            return queryset.filter(author=author)
        return queryset

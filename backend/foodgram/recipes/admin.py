from django.contrib.admin import ModelAdmin, register, TabularInline
from recipes.models import (Tag, Ingredient, Recipe,
                            IngredientRecipe, IngredientRecipe)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class IngredientsInline(TabularInline):
    model = IngredientRecipe
    extra = 1


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'favourite_count')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favourite_count',)
    inlines = (IngredientsInline,)

    def favourite_count(self, obj):
        return obj.favourites.count()


@register(IngredientRecipe)
class IngredientRecipeAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')

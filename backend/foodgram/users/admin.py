from django.contrib.admin import ModelAdmin, register

from users.models import Favourite, Follow, ShoppingList, User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'password')
    list_filter = ('username', 'email')


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('user', 'author')


@register(Favourite)
class FavouriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')


@register(ShoppingList)
class ShoppingListAdmin(ModelAdmin):
    list_display = ('user', 'recipe')

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    email = models.EmailField(
        max_length=254,
        verbose_name='Почта',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='Проверка уникальности подписки',
                fields=('user', 'author')
            ),
            models.CheckConstraint(
                name='Проверка подписки на самого себя',
                check=~models.Q(user=models.F('author'))
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} -> {self.author}'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        default_related_name = 'favourites'
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        default_related_name = 'shopping_list'
        unique_together = ('user', 'recipe')
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} -> {self.recipe}'

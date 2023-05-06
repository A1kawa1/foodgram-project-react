from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.validators import ValidationError


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

    def save(self, *args, **kwargs):
        if self.user == self.author:
            raise ValidationError('Подписка на самого себя')
        if Follow.objects.filter(
            user=self.user,
            author=self.author
        ).exists():
            raise ValidationError('Вы уже подписанны на него')
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'author')

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

    def __str__(self):
        return f'{self.user} -> {self.recipe}'

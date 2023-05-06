from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=60,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^#[A-Fa-f0-9]{6}$',
                flags=0,
                message='Недопустимый цвет'
            )
        ]
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=60,
        unique=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=60,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=15
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Недопустимое значение (меньше единицы)'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now=True
    )

    class Meta:
        default_related_name = 'recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='resipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

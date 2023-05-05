from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import ValidationError
from rest_framework import serializers
from users.models import Follow, Favourite, ShoppingList
from recipes.models import Tag, Ingredient, Recipe, IngredientRecipe
from api.custom_field import Base64ImageField


User = get_user_model()


class MyUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and Follow.objects.filter(
                    user=user,
                    author=obj).exists())


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password')


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()

    def update(self, instance, validated_data):
        print(instance.password)
        if not check_password(validated_data['current_password'], instance.password):
            raise ValidationError('Неверный пароль')
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


class FollowSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)
    recipes = SerializerMethodField(read_only=True)
    recipes_count = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and Follow.objects.filter(
                    user=user,
                    author=obj).exists())

    def get_recipes(self, obj):
        limit = self.context['request'].GET.get('recipes_limit')
        recipe = obj.recipes.all()
        if limit:
            recipe = recipe[:int(limit)]
        return RecipeInfSerializer(recipe, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeInfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = MyUserSerializer(
        read_only=True
    )
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='resipes'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and obj.favourites.filter(
                    user=user
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and obj.shopping_list.filter(
                    user=user
                ).exists())


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = AddIngredientSerializer(
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        if not all([field in data.keys() for field in self.Meta.fields]):
            raise serializers.ValidationError('Нет необходимых полей')
        ingredients = data.get('ingredients')
        if not len(ingredients):
            raise serializers.ValidationError(
                'Список ингридиентов пустой')
        return data

    @staticmethod
    def add_ingredients(recipe, ingredients):
        tmp = {}
        for ingredient in ingredients:
            if tmp.get(ingredient['ingredient']) is None:
                tmp[ingredient['ingredient']] = ingredient['amount']
            else:
                tmp[ingredient['ingredient']] += ingredient['amount']

        data = [
            IngredientRecipe(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            ) for ingredient, amount in tmp.items()
        ]
        IngredientRecipe.objects.bulk_create(data)

    def create(self, validated_data):
        user = self.context['request'].user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=user,
            **validated_data
        )
        recipe.tags.add(*tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.ingredients.clear()
        ingredients = validated_data['ingredients']
        self.add_ingredients(instance, ingredients)
        instance.tags.clear()
        tags = validated_data['tags']
        instance.tags.add(*tags)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return RecipeInfSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class FavoriteSerializer(FavoriteShoppingCartSerializer):
    class Meta:
        model = Favourite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return RecipeInfSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(FavoriteShoppingCartSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return RecipeInfSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data

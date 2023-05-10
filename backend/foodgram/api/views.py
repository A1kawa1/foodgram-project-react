import os

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilterSet, RecipeFilterSet
from api.paginations import LimitResultsSetPagination
from api.permissions import IsAuthOrStaffOrReadOnly
from api.serializers import (FollowSerializer, IngredientSerializer,
                             MyUserSerializer, RecipeInfSerializer,
                             RecipeReadSerializer, RecipeWriteSerializer,
                             SetPasswordSerializer, TagSerializer)
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import Favourite, Follow, ShoppingList

User = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = LimitResultsSetPagination

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        serializer = MyUserSerializer(
            user,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        user = request.user
        serializer = SetPasswordSerializer(
            user,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Пароль изменен'},
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            serializer = FollowSerializer(
                author,
                context={'request': request}
            )
            Follow.objects.create(
                user=user,
                author=author
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        subscription = get_object_or_404(
            Follow,
            user=user,
            author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        following = User.objects.filter(following__user=user)
        page = self.paginate_queryset(following)
        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterSet
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthOrStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    pagination_class = LimitResultsSetPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            _, create = Favourite.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not create:
                return Response(
                    {'errors': 'Рецепт уже добавлен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipeInfSerializer(
                recipe,
                context={'request': request}
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        favorite_resipe = get_object_or_404(
            Favourite,
            user=user,
            recipe=recipe
        )
        favorite_resipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingList.objects.filter(user=user)
        if not shopping_cart.exists():
            return Response(
                {'errors': 'not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_list__user=user
        ).values('ingredient').annotate(total=Sum('amount'))

        data = ''
        for el in ingredients:
            ingredient = Ingredient.objects.get(id=el.get("ingredient"))
            data += ((f'{ingredient} - '
                      f'{el.get("total")} '
                      f'{ingredient.measurement_unit}\n'))

        filename = f'{user.username}.txt'
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            _, create = ShoppingList.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not create:
                return Response(
                    {'errors': 'Рецепт уже добавлен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipeInfSerializer(
                recipe,
                context={'request': request}
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        favorite_resipe = get_object_or_404(
            ShoppingList,
            user=user,
            recipe=recipe
        )
        favorite_resipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

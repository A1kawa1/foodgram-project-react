from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, MyUserViewSet, RecipeViewSet,
                       TagViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', MyUserViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]

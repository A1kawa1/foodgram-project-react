from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import MyUserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet


router = DefaultRouter()
router.register('users', MyUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]

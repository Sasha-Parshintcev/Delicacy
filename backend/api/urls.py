from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    IngredientViewSet,
    DishViewSet,
    UserViewSet
)


api_v1 = DefaultRouter()
api_v1.register('users', UserViewSet, basename='users')
api_v1.register('categories', CategoryViewSet, basename='categories')
api_v1.register('ingredients', IngredientViewSet, basename='ingredients')
api_v1.register('dishes', DishViewSet, basename='dishes')

urlpatterns = [
    path('', include(api_v1.urls)),
    re_path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
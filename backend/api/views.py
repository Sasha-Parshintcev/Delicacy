from rest_framework import viewsets

from food.models import (
    Category,
    Ingredient,
    Dish
)
from .serializers import (
    CategorySerializer,
    IngredientSerializer,
    DishSerializer
)


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import (
    SAFE_METHODS
)

from food.models import (
    Category,
    Ingredient,
    Dish
)
from .serializers import (
    CategorySerializer,
    IngredientSerializer,
    DishSerializer,
    DishCreateSerializer
)

# Право изменять блюдо доступно только администратору
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    # serializer_class = DishSerializer
    # http_method_names = ('get', 'post', 'patch', 'delete')
    
    def get_queryset(self):
        return Dish.objects.prefetch_related('ingredients', 'category').all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return DishSerializer
        return DishCreateSerializer
    
    
class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
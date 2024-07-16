from rest_framework import serializers

from food.models import (
    Category, Ingredient, Dish
)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
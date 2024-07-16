from rest_framework import serializers

from food.models import (
    Category, Ingredient, Dish
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к Category."""

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug'
        )
        

class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name'
        )
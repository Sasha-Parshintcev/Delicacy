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


class DishSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к Dish."""
    ingredients = IngredientSerializer(many=True) # source='',
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = (
            'id',
            'category',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
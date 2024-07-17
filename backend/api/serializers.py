from rest_framework import serializers
from django.core.files.base import ContentFile
import base64

from food.models import (
    Category, Ingredient, Dish, DishIngredient
)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image/png'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
    

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


class DishIngredientWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели DishIngredient.'''
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = DishIngredient
        fields = (
            'id'
        )


class DishCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добаления/обновления блюда."""
    image = Base64ImageField()
    ingredients = DishIngredientWriteSerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )

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

    def create_ingredients(self, dish, ingredients):
        DishIngredient.objects.bulk_create(
            [
                DishIngredient(
                    dish=dish,
                    ingredient=ingredient['id']
                ) for ingredient in ingredients
            ]
        )

    def to_representation(self, instance):
        return DishSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


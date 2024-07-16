from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

TEXT_LENGTH_LIMIT = 20
MODEL_LENGTH_LIMIT = 35


class Category(models.Model):
    """Модель категории блюда."""
    name = models.CharField(
        'Название категории',
        max_length=MODEL_LENGTH_LIMIT,
    )
    slug = models.SlugField(
        'Идентификатор категории',
        max_length=MODEL_LENGTH_LIMIT,
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.name[:TEXT_LENGTH_LIMIT]
    

class Ingredient(models.Model):
    """Модель ингредиента для блюда."""
    name = models.CharField(
        'Название ингредиента',
        help_text='Названия ингридинта для блюда',
        max_length=MODEL_LENGTH_LIMIT,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name',),
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return self.name[:TEXT_LENGTH_LIMIT]
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

TEXT_LENGTH_LIMIT = 35
MODEL_LENGTH_LIMIT = 30
MIN_COOK_TIME = 15


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
    

class Dish(models.Model):
    """Модель блюда."""
    name = models.CharField(
        'Название блюда',
        help_text='Например "От шефа (если речь про шаурму)"',
        max_length=MODEL_LENGTH_LIMIT
    )
    image = models.ImageField(
        'Изображение',
        help_text='Загрузите изображение для блюда',
        upload_to='dishes/',
        null=True,
        default=None
    )
    text = models.TextField(
        'Описание',
        help_text='Описание блюда'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='dishes',
        help_text='Ингредиенты в составе блюда'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='dishes',
        verbose_name='Категория',
        help_text='Можно установить несколько тегов на один рецепт'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Введите время приготовления',
        validators=(
            MinValueValidator(
                MIN_COOK_TIME,
                f'Минимальное время: {MIN_COOK_TIME} минут'
            ),
        )
    )
    class Meta:
        ordering = ['name']
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return f'{self.name}\n{self.text[:TEXT_LENGTH_LIMIT]}'
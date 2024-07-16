from django.db import models
from django.contrib.auth import get_user_model

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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH_LIMIT]
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator


TEXT_LENGTH_LIMIT = 20
MAX_LENGTH_MODEL = 150


class User(AbstractUser):
    """
    Модель User расширяет стандартную модель AbstractUser из Django,
    добавляя возможность добавления аватара пользователя
    и предназначена для хранения информации о пользователях в системе.
    Регистрация пользователей осуществляется с помощью email,
    что позволяет улучшить безопасность
    и облегчить процесс восстановления пароля.
    """
     email = models.EmailField(
        'email-адрес',
        max_length=254,
        unique=True,
    )
    avatar = models.ImageField(
        'аватар',
        upload_to='users/',
        blank=True,
        default=None
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:TEXT_LENGTH_LIMIT]

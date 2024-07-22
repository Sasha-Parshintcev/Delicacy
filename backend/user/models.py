from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


TEXT_LENGTH_LIMIT = 20


class User(AbstractUser):
    """
    Модель пользователя.
    Регистрация с помощью email.
    """
    email = models.EmailField(
        'email-адрес',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
        }
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
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

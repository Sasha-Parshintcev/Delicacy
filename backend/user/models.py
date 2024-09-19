from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator


TEXT_LENGTH_LIMIT = 20
MAX_LENGTH_MODEL = 150


class User(AbstractUser):
    """
    Модель пользователя.
    Регистрация с помощью email.
    """
    email = models.EmailField(
        'email-адрес',
        max_length=MAX_LENGTH_MODEL,
        unique=True,
    )
    username = models.CharField(
        'Логин',
        max_length=MAX_LENGTH_MODEL,
        validators=[UnicodeUsernameValidator()],
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
        }
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH_MODEL
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH_MODEL
    )
    password = models.CharField(
        'Пароль',
        max_length=MAX_LENGTH_MODEL,
    )
    avatar = models.ImageField(
        'аватар',
        upload_to='users/',
        blank=True,
        default=None
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text =('Группы, к которым принадлежит этот пользователь'),
        related_name='custom_user_group'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Особые разрешения для этого пользователя'),
        related_name='custom_user_permissions'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:TEXT_LENGTH_LIMIT]

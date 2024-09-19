import os
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser import views as djoser_views

from user.models import User
from food.models import (
    Category,
    Ingredient,
    Dish
)
from .serializers import (
    CategorySerializer,
    IngredientSerializer,
    DishSerializer,
    DishCreateSerializer,
    UserSerializer,
    AvatarSerializer
)

# Право изменять блюдо доступно только администратору
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    # serializer_class = DishSerializer
    # http_method_names = ('get', 'post', 'patch', 'delete')
    
    def get_queryset(self):
        return Dish.objects.prefetch_related('ingredients', 'category').all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return DishSerializer
        return DishCreateSerializer
    
    
class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
    
class UserViewSet(djoser_views.UserViewSet):
    """
    Вьюсет для работы с пользователями.

    Реализует следующие действия:
    - Получение информации о текущем пользователе
    - Обновление аватара

    Особенности:
    - Используется модель User
    - Применяется сериализатор UserSerializer
    - Доступ разрешен для всех пользователей на чтение и
      для аутентифицированных на изменение
      (permission_classes = (IsAuthenticatedOrReadOnly,))
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(
        detail=False,
        permission_classes=(IsAuthenticatedOrReadOnly,)
    )
    def me(self, request):
        """
        Получить информацию о текущем аутентифицированном пользователе.
        Данный метод возвращает данные пользователя в формате JSON. 
        Доступ к методу имеют только аутентифицированные пользователи.
        """
        serializer = UserSerializer(
            instance=request.user,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(
        methods=('put', 'delete'),
        detail=False,
        url_path='me/avatar'
    )
    def avatar(self, request):
        """
        Обновить или удалить аватар текущего аутентифицированного пользователя.
        Данная функция позволяет аутентифицированному пользователю
        загружать новый аватар (метод PUT) или удалять существующий
        аватар (метод DELETE).
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'detail': 'Учетные данные аутентификации не предоставлены.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = AvatarSerializer(data=request.data)
        if request.method == 'PUT':
            if serializer.is_valid():
                user.avatar = serializer.validated_data['avatar']
                user.save()
                return Response(
                    {"avatar": os.getenv('HOST', '/.env')},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == 'DELETE':
            user.avatar = None
            user.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
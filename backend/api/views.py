from djoser.views import UserViewSet as DjoserUserViewSet
from sales.models import User

from .serializers import UserSerializer


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

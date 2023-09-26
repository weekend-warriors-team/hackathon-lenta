import djoser.serializers

from rest_framework.validators import UniqueTogetherValidator
from .models import User


class UserSerializer(djoser.serializers.UserSerializer):
    '''Сериализатор модели пользователя'''
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]
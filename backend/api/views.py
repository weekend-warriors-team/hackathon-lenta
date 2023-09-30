from categories.models import Category, Group, Product, Subcategory
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from stores.models import Store
from users.models import User

from .serializers import ProductSerializer, StoreSerializer, UserSerializer


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ShopViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с магазинами."""
    http_method_names = ['get']
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'store', 'city', 'division', 'type_format', 'loc', 'size', 'is_active'
    ]


class ProductViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с продуктами."""
    http_method_names = ['get']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'subcategory', 'uom'
    ]

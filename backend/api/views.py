from categories.models import Category, Group, Product, Subcategory
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.response import Response
from sales.models import Sale
from sales_forecasts.models import Forecast
from stores.models import Store
from users.models import User

from .filters import ForecastFilter
from .serializers import (ForecastSerializer, ProductSerializer,
                          SalesSerializer, StoreSerializer, UserSerializer)


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


class SaleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с продажами."""
    http_method_names = ['get']
    queryset = Sale.objects.all().distinct('store', 'sku')
    serializer_class = SalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'sku']


class ForecastViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с прогнозами."""
    http_method_names = ['get']
    queryset = (
        Forecast.objects.all().select_related('store', 'sku')
        .distinct('store', 'sku', 'forecast_date').order_by('forecast_date')
    )
    serializer_class = ForecastSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ForecastFilter

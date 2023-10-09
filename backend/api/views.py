from api.services import all_data_to_files, forecasts_loader
from categories.models import Product
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from sales.models import Sale
from sales_forecasts.models import Forecast
from stores.models import Store
from users.models import User

from .filters import ForecastFilter
from .serializers import (ForecastSerializer, ProductSerializer,
                          SalesSerializer, StoreSerializer, UserSerializer)

MAX_ROWS = 1000


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

    @action(methods=['post'], detail=False,)
    def add_daily_forecast(self, request):
        """Загружает в БД данные о прогнозе продаж по дням."""
        return forecasts_loader()

    def allow_methods(self, request, *args, **kwargs):
        """Разрешает метод 'POST' только для добавления
        прогноза продаж из файла csv."""
        if self.action == 'add_daily_forecast':
            return ['post']
        return super().allow_methods(request, *args, **kwargs)


class DataToFileViewSet(viewsets.ViewSet):
    """Вьюсет для загагрузки данных в csv."""

    def list(self, request):
        """Скачивает данные о продажах в csv."""
        return all_data_to_files(request)

import csv

from categories.models import Category, Group, Product, Subcategory
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sales.models import Sale
from sales_forecasts.models import Forecast
from stores.models import Store
from users.models import User

from .filters import ForecastFilter
from .serializers import (ForecastSerializer, ProductSerializer,
                          SalesSerializer, StoreSerializer, UserSerializer)

sales_headers = [
    'st_id', 'pr_sku_id', 'date', 'pr_sales_type_id',
    'pr_sales_in_units', 'pr_promo_sales_in_units',
    'pr_sales_in_rub', 'pr_promo_sales_in_rub'
]

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

    @action(
            detail=False, methods=['get'], permission_classes=[IsAuthenticated]
    )
    def sales_data_to_file(self, request):
        """Скачивает данные о продажах в csv."""
        file_name = '/backend_static/' + request.GET.get('file_name') + '.csv'
        queryset = Sale.objects.all().order_by('store', 'sku', 'date')
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(sales_headers)
            # получаем список полей модели Sale
            fields = [
                field for field in Sale._meta.get_fields()
                if field.name != 'id'
            ]
            rows = []
            counter = 0
            for sale in queryset:
                rows.append(
                    [
                        getattr(sale, field.name) if field.name != 'sales_type'
                        else int(getattr(sale, field.name)) for field in fields
                    ]
                )
                counter += 1
                if len(rows) >= MAX_ROWS:
                    writer.writerows(rows)
                    rows = []
            if rows:
                writer.writerows(rows)
        print(f'Продажи записаны в файл {file_name}. Всего строк: {counter}')
        return Response(status=status.HTTP_200_OK)


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

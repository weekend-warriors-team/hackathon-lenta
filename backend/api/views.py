from rest_framework import status
from rest_framework.response import Response
from categories.models import Category, Group, Product, Subcategory
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from sales.models import Sale
from stores.models import Store
from users.models import User
from sales_forecasts.models import Forecast, ForecastSku, ForecastDaily

from .serializers import (ProductSerializer, SalesSerializer, StoreSerializer,
                          UserSerializer, ForecastSerializer, ForecastSkuSerializer, ForecastDailySerializer)


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
    serializer_class = SalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'sku']

    def get_queryset(self):
        queryset = Sale.objects.all().distinct('store', 'sku')
        filtered_queryset = self.filter_queryset(queryset)
        return filtered_queryset


class ForecastViewSet(viewsets.ModelViewSet):
    '''Вьюсет для работы с прогнозами'''
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'forecast_date']

    def list(self, request):
        forecasts = self.queryset
        serializer = self.serializer_class(forecasts, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            forecast = self.queryset.get(pk=pk)
        except Forecast.DoesNotExist:
            return Response({'error': 'Прогноз не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(forecast)
        return Response(serializer.data)

    
class ForecastSkuViewSet(viewsets.ModelViewSet):
    '''Вьюсет прогнозов товаров'''
    queryset = ForecastSku.objects.all()
    serializer_class = ForecastSkuSerializer

    def list(self, request):
        forecasts_sku = self.queryset
        serializer = self.serializer_class(forecasts_sku, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            forecast_sku = self.queryset.get(pk=pk)
        except ForecastSku.DoesNotExist:
            return Response({'error': 'Прогноз товара не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(forecast_sku)
        return Response(serializer.data)


class ForecastDailyViewSet(viewsets.ModelViewSet):
    '''Вьюсет ежедневных прогнозов'''
    queryset = ForecastDaily.objects.all()
    serializer_class = ForecastDailySerializer

    def list(self, request):
        forecasts_daily = self.queryset
        serializer = self.serializer_class(forecasts_daily, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            forecast_daily = self.queryset.get(pk=pk)
        except ForecastDaily.DoesNotExist:
            return Response({'error': 'Ежедневный прогноз не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(forecast_daily)
        return Response(serializer.data)

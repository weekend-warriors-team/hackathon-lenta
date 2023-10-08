from categories.models import Category, Group, Product, Subcategory
from rest_framework import serializers
from sales.models import Sale
from sales_forecasts.models import Forecast
from stores.models import Store
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователей"""

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Создает нового пользователя."""
        user = User.objects.create_user(**validated_data)
        return user


class GroupSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Group.'''
    class Meta:
        model = Group
        fields = ('title',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    group = GroupSerializer()

    class Meta:
        model = Category
        fields = ('title', 'group')


class SubcategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Subcategory'''

    category = CategorySerializer()

    class Meta:
        model = Subcategory
        fields = ('title', 'category')


class ProductSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Category.'''

    category = serializers.CharField(source='subcategory.category.title')
    group = serializers.CharField(source='subcategory.category.group.title')

    class Meta:
        fields = ('sku', 'group', 'category', 'subcategory', 'uom')
        model = Product


class StoreSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Store.'''
    class Meta:
        fields = ('store', 'city', 'division',
                  'type_format', 'loc', 'size',
                  'is_active')
        model = Store


class SalesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sale."""
    fact = serializers.SerializerMethodField()

    class Meta:
        fields = ('store', 'sku', 'fact')
        read_only_fields = ('store', 'sku', 'fact')
        model = Sale

    def get_fact(self, obj):
        """Возвращает данные о продажах товара в магазине по дням."""
        fact = []
        store_sku_sales = Sale.objects.all().filter(
            store=obj.store, sku=obj.sku
        ).order_by('date')
        for sale in store_sku_sales:
            sale_fact = {
                "date": sale.date,
                "sales_type": sale.sales_type,
                "sales_units": sale.sales_units,
                "sales_units_promo": sale.sales_units_promo,
                "sales_rub": sale.sales_rub,
                "sales_rub_promo": sale.sales_rub_promo
            }
            fact.append(sale_fact)
        return fact


class ForecastSerializer(serializers.ModelSerializer):
    """Сериализатор для модели прогноза данных."""
    forecast = serializers.SerializerMethodField()

    class Meta:
        fields = ('store', 'sku', 'forecast_date', 'forecast')
        model = Forecast

    def get_forecast(self, obj):
        """Возвращает данные о прогнозе продаж по дням"""
        forecasts = {}
        store_sku_forecasts = Forecast.objects.all().filter(
            store=obj.store,
            sku=obj.sku,
            forecast_date=obj.forecast_date
        )
        for forecast in store_sku_forecasts:
            forecasts[forecast.date.strftime('%Y-%m-%d')] = forecast.target
        return forecasts

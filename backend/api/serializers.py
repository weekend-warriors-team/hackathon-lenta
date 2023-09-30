from categories.models import Category, Group, Subcategory
from django.utils import timezone
from rest_framework import serializers
from sales.models import Sale
from sales_forecasts.models import Forecast, ForecastDaily, ForecastSku
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


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Category.'''
    class Meta:
        fields = ('sku', 'group', 'category', 'subcategory', 'uom')
        model = Category


class GroupSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Group'''
    class Meta:
        fields = ('id', 'group')
        model = Group


class SubcategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Subcategory'''
    class Meta:
        fields = ('subcategory', 'category')
        model = Subcategory


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

    def get_fact(self, store, sku):
        """Возвращает данные о продажах товара в магазине по дням."""
        fact = []
        store_sku_sales = Sale.objects.all().filter(store=store, sku=sku)
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
    '''Сериализатор для модели прогноза данных'''
    class Meta:
        model = Forecast
        fields = ['id', 'store', 'forecast_date']

    def validate(self, data):
        if data['forecast_date'] < timezone.now().date():
            raise serializers.ValidationError('Дата прогноза не может быть в прошлом')
        return data

    def create(self, validated_data):
        forecast = Forecast.objects.create(**validated_data)
        return forecast

    def update(self, instance, validated_data):
        instance.store = validated_data.get('store', instance.store)
        instance.forecast_date = validated_data.get('forecast_date', instance.forecast_date)
        instance.save()
        return instance
    

class ForecastSkuSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели прогноза товара'''
    class Meta:
        model = ForecastSku
        fields = ['id', 'forecast', 'sku']

    def create(self, validated_data):
        forecast_sku = ForecastSku.objects.create(**validated_data)
        return forecast_sku

    def update(self, instance, validated_data):
        instance.forecast = validated_data.get('forecast', instance.forecast)
        instance.sku = validated_data.get('sku', instance.sku)
        instance.save()
        return instance


class ForecastDailySerializer(serializers.ModelSerializer):
    '''Сериализатор для модели ежедневного прогноза'''
    class Meta:
        model = ForecastDaily
        fields = '__all__'



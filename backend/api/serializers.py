from rest_framework import serializers
from django.utils import timezone

from categories.models import Category, Group, Subcategory
from sales.models import Sales, SalesRecord
from stores.models import Stores
from sales_forecasts.models import Forecast, ForecastSku, ForecastDaily
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
    '''Сериализатор для модели Category'''
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


class SalesSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Sales'''
    store = serializers.PrimaryKeyRelatedField(
        queryset=Stores.objects.all()
    )
    sku = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('store', 'sku')
        model = Sales


class SalesRecordSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели SalesRecord'''
    class Meta:
        fields = ('fact', 'date', 'sales_type', 'sales_units', 'sales_units_promo',
                  'sales_rub', 'sales_rub_promo')
        model = SalesRecord


class StoreSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Store'''
    class Meta:
        fields = ('store_name', 'city', 'division',
                  'type_format', 'loc', 'size',
                  'is_active')
        model = Stores


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

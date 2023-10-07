# from api.services import sales_data_to_file
from api.views import (DataToFileViewSet, ForecastViewSet, ProductViewSet,
                       SaleViewSet, ShopViewSet, UserViewSet)
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
router.register('shops', ShopViewSet, 'shops')
router.register('products', ProductViewSet, 'products')
router.register('sales', SaleViewSet, 'sales')
router.register('forecast', ForecastViewSet, 'forecast')
router.register('data_to_file', DataToFileViewSet, 'data_to_file')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    # path('data_to_file/', sales_data_to_file, name='data_to_file'),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

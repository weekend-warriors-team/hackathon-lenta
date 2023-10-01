from api.views import ProductViewSet, SaleViewSet, ShopViewSet, UserViewSet
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
router.register('shops', ShopViewSet, 'shops')
router.register('products', ProductViewSet, 'products')
router.register('sales', SaleViewSet, 'sales')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

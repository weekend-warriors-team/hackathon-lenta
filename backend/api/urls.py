from api.views import ShopsViewSet, UserViewSet
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
router.register('shops', ShopsViewSet, 'shops')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

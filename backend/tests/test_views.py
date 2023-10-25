from datetime import date
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from categories.models import Category, Product
from sales.models import Sale
from stores.models import Store


class ProductViewAPITest(TestCase):
    '''Тестирование вьюсета для работы с продуктами'''
    def setUp(self):
        self.client = APIClient()
        self.product_data = {
            'name': 'Test Product',
            'category': 'Test Category',
            'subcategory': 'Test Subcategory',
            'uom': 'Test UOM',
            'price': 10.0,
            'description': 'Test Description'
        }
        self.product = Product.objects.create(**self.product_data)

    def test_get_product_list(self):
        response = self.client.get('/api/v1/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_product(self):
        response = self.client.get(f"/api/v1/products/{self.product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Test Product")

    def test_products_by_subcategory(self):
        response = self.client.get("/api/v1/products/?subcategory=Test Subcategory")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_products_by_uom(self):
        response = self.client.get("/api/v1/products/?uom=Test UOM")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ShopViewAPITest(TestCase):
    '''Тестирование вьюсета для работы с магазинами '''
    def setUp(self):
        self.client = APIClient()
        self.store_data = {
            'store': 'Test Store',
            'city': 'Test City',
            'division': 'Test Division',
            'type_format': 1,
            'loc': 1,
            'size': 1,
            'is_active': 'True'
        }
        self.store = Store.objects.create(**self.store_data)

    def test_get_store_list(self):
        response = self.client.get('/api/v1/shops')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    
    def test_get_store(self):
        response = self.client.get(f"/api/v1/shops/{self.store.store}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["store"], "TestStore")

    def test_stores_by_type_format(self):
        response = self.client.get("/api/v1/shops/?type_format=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_stores_by_loc(self):
        response = self.client.get("/api/v1/shops/?loc=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_stores_by_city(self):
        response = self.client.get("/api/v1/shops/?city=TestCity")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_stores_by_division(self):
        response = self.client.get("/api/v1/shops/?division=TestDivision")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class SaleViewAPITest(TestCase):
    '''Тестирование вьюсета для работы с продажами'''

    def setUp(self):
        self.client = APIClient()
        self.store = Store.objects.create(store="Test Store")
        self.category = Category.objects.create(sku="Test SKU")
        self.sale_data = {
            "store": self.store,
            "sku": self.category,
            "date": date.today(),
            "sales_type": True,
            "sales_units": 10,
            "sales_units_promo": 5,
            "sales_rub": 100.0,
            "sales_run_promo": 50.0,
        }
        Sale.objects.create(**self.sale_data)

    def test_list_sales(self):
        response = self.client.get("/api/v1/sales/", {"store": self.store.store})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["store"], "Test Store")

    def test_retrieve_sale(self):
        response = self.client.get(
            f"/api/v1/sales/{self.category.sku}/",
            {"store": self.store.store, "sku": self.category.sku},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["store"], "Test Store")
        self.assertEqual(response.data["sku"], "Test SKU")

    
    class ForecastViewAPITest(TestCase):
        '''Тестирование вьюсета для работы с прогнозами'''

    def setUp(self):
        self.client = APIClient()
        self.store = Store.objects.create(store="Test Store", city="Test City")
        self.category = Category.objects.create(sku="Test SKU", group="Test Group")

    def test_forecast_by_store(self):
        url = reverse("forecast-list")
        response = self.client.get(url, {"store": "Test Store"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_forecast_by_sku(self):
        url = reverse("forecast-list")
        response = self.client.get(url, {"sku": "Test SKU"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

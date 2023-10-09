from django.test import TestCase
from django.core.exceptions import ValidationError
from sales.models import Sale
from stores.models import Store, City, Division
from categories.models import Group, Category, Subcategory, Product
from sales_forecasts.models import Forecast


class GroupTestCase(TestCase):
    '''Тестирование модели групп'''
    def setUp(self):
        self.group = Group.objects.create(
            title='Test Group',
        )

    def test_group_title(self):
        self.assertEqual(str(self.group), 'Test Group')
        self.assertEqual(self.group.title, 'Test Group')

    def test_group_verbose_name(self):
        self.assertEqual(Group._meta.verbose_name, 'Группа')
        self.assertEqual(Group._meta.verbose_name_plural, 'Группы')

    def test_group_ordering(self):
        self.assertEqual(Group._meta.ordering, ['title'])


class CategoryTestCase(TestCase):
    '''Тестирование модели категорий'''
    def setUp(self):
        self.group = Group.objects.create(
            title='Test Group',
        )
        self.category = Category.objects.create(
            title='Test Category',
            group=self.group,
        )

    def test_category_title(self):
        self.assertEqual(str(self.category), 'Test Category')
        self.assertEqual(self.category.title, 'Test Category')

    def test_category_group(self):
        self.assertEqual(self.category.group, self.group)

    def test_category_verbose_name(self):
        self.assertEqual(Category._meta.verbose_name, 'Категория')
        self.assertEqual(Category._meta.verbose_name_plural, 'Категории')

    def test_category_ordering(self):
        self.assertEqual(Category._meta.ordering, ['title'])


class SubcategoryTestCase(TestCase):
    '''Тестирование модели подкатегорий'''
    def setUp(self):
        self.group = Group.objects.create(
            title='Test Group',
        )
        self.category = Category.objects.create(
            title='Test Category',
            group=self.group,
        )
        self.subcategory = Subcategory.objects.create(
            title='Test Subcategory',
            category=self.category,
        )

    def test_subcategory_title(self):
        self.assertEqual(str(self.subcategory), 'Test Subcategory')
        self.assertEqual(self.subcategory.title, 'Test Subcategory')

    def test_subcategory_category(self):
        self.assertEqual(self.subcategory.category, self.category)

    def test_subcategory_verbose_name(self):
        self.assertEqual(Subcategory._meta.verbose_name, 'Подкатегория')
        self.assertEqual(Subcategory._meta.verbose_name_plural, 'Подкатегории')

    def test_subcategory_ordering(self):
        self.assertEqual(Subcategory._meta.ordering, ['title'])


class ProductTestCase(TestCase):
    '''Тестирование модели продуктов'''
    def setUp(self):
        self.group = Group.objects.create(
            title='Test Group',
        )
        self.category = Category.objects.create(
            title='Test Category',
            group=self.group,
        )
        self.subcategory = Subcategory.objects.create(
            title='Test Subcategory',
            category=self.category,
        )
        self.product = Product.objects.create(
            sku='Test Product',
            subcategory=self.subcategory,
        )

    def test_product_sku(self):
        self.assertEqual(str(self.product), 'Test Product')
        self.assertEqual(self.product.sku, 'Test Product')

    def test_product_subcategory(self):
        self.assertEqual(self.product.subcategory, self.subcategory)

    def test_product_verbose_name(self):
        self.assertEqual(Product._meta.verbose_name, 'Продукт')
        self.assertEqual(Product._meta.verbose_name_plural, 'Продукты')

    def test_product_ordering(self):
        self.assertEqual(Product._meta.ordering, ['sku'])


class SaleModelTestCase(TestCase):
    '''Тестирование модели продаж'''
    def setUp(self):
        self.store = Store.objects.create(name='Test Store')
        self.product = Product.objects.create(sku='Test Product')
        self.sale = Sale.objects.create(
            store=self.store,
            sku=self.product,
            date='2023-07-19',
            sales_type=True,
            sales_units=10,
            sales_units_promo=5,
            sales_rub=1000,
            sales_rub_promo=500
        )

    def test_sale_store(self):
        self.assertEqual(self.sale.store, self.store)

    def test_sale_sku(self):
        self.assertEqual(self.sale.sku, self.product)

    def test_sale_date(self):
        self.assertEqual(str(self.sale.date), '2023-07-19')

    def test_sale_sales_type(self):
        self.assertTrue(self.sale.sales_type)

    def test_sale_sales_units(self):
        self.assertEqual(self.sale.sales_units, 10)

    def test_sale_sales_units_promo(self):
        self.assertEqual(self.sale.sales_units_promo, 5)

    def test_sale_sales_rub(self):
        self.assertEqual(self.sale.sales_rub, 1000)

    def test_sale_sales_rub_promo(self):
        self.assertEqual(self.sale.sales_rub_promo, 500)

    def test_sale_str(self):
        self.assertEqual(str(self.sale), 'Test Store-Test Product-2023-07-19')


class StoreTestCase(TestCase):
    '''Тестирование модели магазинов'''
    def setUp(self):
        self.city = City.objects.create(city='Test City')
        self.division = Division.objects.create(division='Test Division')
        self.store = Store.objects.create(
            store='Test Store',
            city=self.city,
            division=self.division,
            type_format=1,
            loc=1,
            size=100,
            is_active=True,
        )

    def test_store_title(self):
        self.assertEqual(str(self.store), 'Test Store')
        self.assertEqual(self.store.store, 'Test Store')

    def test_store_city(self):
        self.assertEqual(str(self.store.city), 'Test City')
        self.assertEqual(self.store.city.city, 'Test City')

    def test_store_division(self):
        self.assertEqual(str(self.store.division), 'Test Division')
        self.assertEqual(self.store.division.division, 'Test Division')

    def test_store_type_format(self):
        self.assertEqual(self.store.type_format, 1)

    def test_store_loc(self):
        self.assertEqual(self.store.loc, 1)

    def test_store_size(self):
        self.assertEqual(self.store.size, 100)

    def test_store_is_active(self):
        self.assertTrue(self.store.is_active)

    def test_store_verbose_name(self):
        self.assertEqual(Store._meta.verbose_name, 'Магазин')
        self.assertEqual(Store._meta.verbose_name_plural, 'Магазины')

    def test_store_ordering(self):
        self.assertEqual(Store._meta.ordering, ['store'])


class ForecastTestCase(TestCase):
    '''Тестирование модели прогнозов'''
    def setUp(self):
        self.store = Store.objects.create(
            name='Test Store',
            address='Test Address',
        )
        self.product = Product.objects.create(
            sku='Test Product',
        )
        self.forecast = Forecast.objects.create(
            forecast_date='2023-07-19',
            store=self.store,
            sku=self.product,
            date='2023-07-19',
            target=10,
        )

    def test_forecast_str(self):
        self.assertEqual(str(self.forecast), 'Test Store-Test Product-2022-01-02')

    def test_forecast_verbose_name(self):
        self.assertEqual(Forecast._meta.verbose_name, 'Прогноз продажи продукта')
        self.assertEqual(Forecast._meta.verbose_name_plural, 'Прогнозы продаж')

    def test_forecast_ordering(self):
        self.assertEqual(Forecast._meta.ordering, ['forecast_date', 'store', 'sku', 'date'])

    def test_forecast_store(self):
        self.assertEqual(self.forecast.store, self.store)

    def test_forecast_sku(self):
        self.assertEqual(self.forecast.sku, self.product)

    def test_forecast_date(self):
        self.assertEqual(str(self.forecast.date), '2022-01-02')

    def test_forecast_target(self):
        self.assertEqual(self.forecast.target, 10)

    def test_forecast_store_delete(self):
        self.store.delete()
        with self.assertRaises(Forecast.DoesNotExist):
            Forecast.objects.get(pk=self.forecast.pk)

    def test_forecast_product_delete(self):
        self.product.delete()
        with self.assertRaises(Forecast.DoesNotExist):
            Forecast.objects.get(pk=self.forecast.pk)

    def test_forecast_negative_target(self):
        self.forecast.target = -1
        with self.assertRaises(ValidationError):
            self.forecast.full_clean()

    def test_forecast_zero_target(self):
        self.forecast.target = 0
        self.forecast.full_clean()

    def test_forecast_null_target(self):
        self.forecast.target = None
        with self.assertRaises(ValidationError):
            self.forecast.full_clean()

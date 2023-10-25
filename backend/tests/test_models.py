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
            title='Group',
        )

    def test_group_title(self):
        self.assertEqual(str(self.group), 'Group')
        self.assertEqual(self.group.title, 'Group')

    def test_group_verbose_name(self):
        self.assertEqual(Group._meta.verbose_name, 'Группа')
        self.assertEqual(Group._meta.verbose_name_plural, 'Группы')

    def test_group_ordering(self):
        self.assertEqual(Group._meta.ordering, ['title'])


class CategoryTestCase(TestCase):
    '''Тестирование модели категорий'''
    def setUp(self):
        self.group = Group.objects.create(
            title='Group',
        )
        self.category = Category.objects.create(
            title='Category',
            group=self.group,
        )

    def test_category_title(self):
        self.assertEqual(str(self.category), 'Category')
        self.assertEqual(self.category.title, 'Category')

    def test_category_group(self):
        self.assertEqual(self.category.group, self.group)

    def test_category_verbose_name(self):
        self.assertEqual(Category._meta.verbose_name, 'Категория')
        self.assertEqual(Category._meta.verbose_name_plural, 'Категории')

    def test_category_ordering(self):
        self.assertEqual(Category._meta.ordering, ['title'])


class SubcategoryTest(TestCase):
    '''Тестирование модели подкатегорий'''
    def setUp(self):
        self.group = Group.objects.create(
            title='Group',
        )
        self.category = Category.objects.create(
            title='Category',
            group=self.group,
        )
        self.subcategory = Subcategory.objects.create(
            title='Subcategory',
            category=self.category,
        )

    def test_subcategory_title(self):
        self.assertEqual(str(self.subcategory), 'Subcategory')
        self.assertEqual(self.subcategory.title, 'Subcategory')

    def test_subcategory_category(self):
        self.assertEqual(self.subcategory.category, self.category)

    def test_subcategory_verbose_name(self):
        self.assertEqual(Subcategory._meta.verbose_name, 'Подкатегория')
        self.assertEqual(Subcategory._meta.verbose_name_plural, 'Подкатегории')

    def test_subcategory_ordering(self):
        self.assertEqual(Subcategory._meta.ordering, ['title'])


class StoreModelTestCase(TestCase):
    '''Тестирование для модели магазинов'''
    def setUp(self):
        self.city = City.objects.create(city='city')
        self.division = Division.objects.create(division='division')
        self.store = Store.objects.create(
            store='store',
            city=self.city,
            division=self.division,
            type_format=1,
            loc=2,
            size=3,
            is_active=True,
        )

    def test_create_store(self):
        self.assertEqual(self.store.store, 'store')
        self.assertEqual(self.store.city, self.city)
        self.assertEqual(self.store.division, self.division)
        self.assertEqual(self.store.type_format, 1)
        self.assertEqual(self.store.loc, 2)
        self.assertEqual(self.store.size, 3)
        self.assertTrue(self.store.is_active)

    def test_store_verbose_name(self):
        self.assertEqual(Store._meta.verbose_name, 'Магазин')
        self.assertEqual(Store._meta.verbose_name_plural, 'Магазины')

    def test_store_ordering(self):
        self.assertEqual(Store._meta.ordering, ('store',))


class SalesModelTestCase(TestCase):
    '''Тестирование модели продаж'''
    def setUp(self):
        self.city = City.objects.create(city='city')
        self.division = Division.objects.create(division='division')
        self.store = Store.objects.create(
            store='store',
            city=self.city,
            division=self.division,
            type_format=1,
            loc=2,
            size=3,
            is_active=True,
        )
        self.sku = Product.objects.create(sku='sku')
        self.sale = Sale.objects.create(
            store=self.store,
            sku=self.sku,
            date='2022-07-19',
            sales_type=True,
            sales_units=10,
            sales_units_promo=5,
            sales_rub=10,
            sales_rub_promo=5,
        )

    def test_create_sale(self):
        self.assertEqual(self.sale.date, '2022-07-19')
        self.assertEqual(self.sale.sales_type, True)
        self.assertEqual(self.sale.sales_units, 10)
        self.assertEqual(self.sale.sales_units_promo, 5)
        self.assertEqual(self.sale.sales_rub, 10)
        self.assertEqual(self.sale.sales_rub_promo, 5)

    def test_sale_verbose_name(self):
        self.assertEqual(Sale._meta.verbose_name, 'Продажа продукта')
        self.assertEqual(Sale._meta.verbose_name_plural, 'Продажи продуктов')


class ForecastModelTestCase(TestCase):
    '''Тестирование модели прогнозов'''
    def setUp(self):
        self.city = City.objects.create(city='city')
        self.division = Division.objects.create(division='division')
        self.store = Store.objects.create(
            store='store',
            city=self.city,
            division=self.division,
            type_format=1,
            loc=2,
            size=3,
            is_active=True,
        )
        self.sku = Product.objects.create(sku='sku')
        self.forecast = Forecast.objects.create(
            store=self.store,
            sku=self.sku,
            forecast_date='2023-03-15',
            date='2023-09-13',
            target=0
        )

    def test_forecast_create(self):
        self.assertEqual(self.forecast.forecast_date,'2023-03-15')
        self.assertEqual(self.forecast.date, '2023-09-13')
        self.assertEqual(self.forecast.target, 0)

    def test_forecast_verbose_name(self):
        self.assertEqual(Forecast._meta.verbose_name, 'Прогноз продажи продукта')
        self.assertEqual(Forecast._meta.verbose_name_plural, 'Прогнозы продаж')

    def test_forecast_ordering(self):
        self.assertEqual(Forecast._meta.ordering, ['forecast_date', 'store', 'sku', 'date'])
    
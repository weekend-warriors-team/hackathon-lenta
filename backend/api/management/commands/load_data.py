from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand
from sales_forecasts.models import Category, Group, Product, Subcategory

data_dir = settings.BASE_DIR/'initial_data'


csv_files = [
    {'model': Group, 'filename': 'pr_df.csv',
     'fieldnames': ['pass', 'title']},
    {'model': Category, 'filename': 'pr_df.csv',
     'fieldnames': ['pass', 'group', 'title']},
    #{'model': Title, 'filename': 'titles.csv',
    # 'fieldnames': ['id', 'name', 'year', 'category_id']},
    #{'model': Review, 'filename': 'review.csv',
    # 'fieldnames': ['id', 'title_id', 'text',
    #                'author_id', 'score', 'pub_date']},
    #{'model': Comment, 'filename': 'comments.csv',
    # 'fieldnames': ['id', 'review_id', 'text', 'author_id', 'pub_date']},
]


class Command(BaseCommand):
    help = "Загружает данные из файлов csv"

    def add_group(self, row):
        """Создает или обновляет группу."""
        Group.objects.update_or_create(title=row['title'],)

    def add_category(self, row):
        """Создает или обновляет категорию."""
        Category.objects.update_or_create(
            title=row['title'],
            group=Group.objects.filter(title=row['group']).first(),
        )

    def csv_loader(self, cf):
        csv_file = f'{data_dir}\\{cf["filename"]}'
        with open(csv_file, encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile, fieldnames=cf['fieldnames'])
            print(f'Загрузка в таблицу модели {cf["model"].__name__}')

            if cf['model'] == Group:
                create_func = self.add_group
            elif cf['model'] == Category:
                create_func = self.add_category

            i, err, r = 0, 0, 0
            next(reader)
            for row in reader:
                try:
                    create_func(row)
                    r += 1
                except Exception as error:
                    print(row)
                    print(
                        f'Ошибка записи в таблицу модели '
                        f'{cf["model"].__name__}, '
                        f'{str(error)}')
                    err += 1
                i += 1
            print(
                f'Всего: {i} строк. Загружено: {r} строк. '
                f'Ошибки: {err} строк.')

    def handle(self, *args, **options):
        print("Идет загрузка данных")
        for сf in csv_files:
            self.csv_loader(сf)
        print('Загрука завершена.')

import csv
import os

from django.core.management.base import BaseCommand

from foodgram_backend.settings import CSV_FILES_DIR
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загружает данные из файла tags.csv в БД'

    def handle(self, *args, **options):
        csv_file = 'tags.csv'
        csv_path = os.path.join(CSV_FILES_DIR, 'tags.csv')
        fieldnames = ['name', 'slug']
        try:
            with open(csv_path, encoding='utf-8') as f:
                reader = csv.DictReader(f, fieldnames)
                for row in reader:
                    Tag(**row).save()
            print(f'Данные из файла {csv_file} успешно загружены.')
        except FileNotFoundError:
            print(f'Файл {csv_file} не найден.')

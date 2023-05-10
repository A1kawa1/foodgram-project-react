import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    text = 'import data from json file'

    def handle(self, *args, **options):
        with open('data/ingredients.json', encoding='utf-8') as file:
            data = json.load(file)
            for record in data:
                try:
                    Ingredient.objects.get_or_create(
                        name=record['name'],
                        measurement_unit=record['measurement_unit']
                    )
                except:
                    ...

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Load ingredients to DB"

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, "data/ingredients.csv")
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                Ingredient.objects.get_or_create(name=row[0], measurement_unit=row[1])

        self.stdout.write("Engredients uploaded.")

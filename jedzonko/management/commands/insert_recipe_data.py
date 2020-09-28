from django.core.management import BaseCommand

from jedzonko.management.commands_data.recipe_data import RECIPE_DATA
from jedzonko.models import Recipe


def insert_recipes():
    for name, ingredients, description, preparation_time in RECIPE_DATA:
        Recipe.objects.create(name=name,
                              ingredients=ingredients,
                              description=description,
                              preparation_time=preparation_time)


class Command(BaseCommand):
    help = "Insert recipe data to database"

    def handle(self, *args, **kwargs):
        insert_recipes()
        print("Data load successfully!")

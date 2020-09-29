from django.core.management import BaseCommand

from jedzonko.management.commands_data.plan_data import PLAN_DATA
from jedzonko.models import Plan


def insert_plans():
    for name, description, in PLAN_DATA:
        Plan.objects.create(name=name,
                            description=description,)


class Command(BaseCommand):
    help = "Insert plans data to database"

    def handle(self, *args, **kwargs):
        insert_plans()
        print("Plans Data load successfully!")

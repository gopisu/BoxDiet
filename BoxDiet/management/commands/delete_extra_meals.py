
from django.core.management.base import BaseCommand
from BoxDiet.models import Meal


class Command(BaseCommand):
    help = 'delete meals with no ranking'

    def handle(self, *args, **options):

        meals = Meal.objects.all()
        for meal in meals:
            if meal.no_of_ranks == 0:
                meal.delete()
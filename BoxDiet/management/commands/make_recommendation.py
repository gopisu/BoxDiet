
from django.core.management.base import BaseCommand, CommandError
from BoxDiet.models import Recommended, User
from BoxDiet.reccomender import give_reccomendations


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        Recommended.objects.all().delete()
        users = User.objects.all()
        for user in users:
            recs = give_reccomendations(user.id)
            for rec in recs:
                Recommended.objects.create(user=user, meal_id=rec['meal__id'], predicted_mark=rec['score'])
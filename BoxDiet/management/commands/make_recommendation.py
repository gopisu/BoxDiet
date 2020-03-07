from django.core.management.base import BaseCommand

from BoxDiet.models import Recommended, User
from BoxDiet.reccomender import give_reccomendations, prepare_rec


class Command(BaseCommand):
    help = "add reccomended meals to all users"

    def handle(self, *args, **options):
        Recommended.objects.all().delete()
        users = User.objects.all()
        model2, items = prepare_rec()
        for user in users:
            recs = give_reccomendations(user.id, model2, items)
            for rec in recs:
                Recommended.objects.create(
                    user=user, meal_id=rec["meal_id"], predicted_mark=rec["score"]
                )

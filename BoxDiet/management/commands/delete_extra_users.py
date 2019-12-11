
from django.core.management.base import BaseCommand, CommandError
from BoxDiet.models import Recommended, User


class Command(BaseCommand):
    help = 'delete users with no ranking'

    def handle(self, *args, **options):

        users = User.objects.all()
        for user in users:
            if user.no_of_given_ranks()['mark__count'] == 0:
                instance = User.objects.get(id=user.id)
                instance.delete()
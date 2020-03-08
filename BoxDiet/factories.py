import factory
from factory.django import DjangoModelFactory

from BoxDiet.models import Meal


class MealFactory(DjangoModelFactory):
    name = factory.Sequence('test_meal{}'.format)
    meal_id = factory.Sequence(lambda n: n)

    class Meta:
        model = Meal

from django.db import models

# Create your models here.
from django.db.models import Avg, Count


class User(models.Model):
    SEX = (
        ('w', 'Kobieta '),
        ('m', 'Mężczyzna'),
        ('\\N', "Brak danych"),
    )
    id = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=5, choices=SEX)

    def avg_of_given_ranks(self):
        # returns None if no rank is related to this instance
        temp = self.meals_user.aggregate(Avg('mark'))
        if temp['mark__avg'] is None:
            return 0.0
        return float(temp['mark__avg'])

    def no_of_given_ranks(self):
        # returns None if no rank is related to this instance
        return self.meals_user.aggregate(Count('mark'))

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return str(self.id)


class Meal(models.Model):
    meal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=246)
    average_rank = models.FloatField(null=True, default=None)
    no_of_ranks = models.IntegerField(null=True, default=0)
    calories_summary = models.FloatField()
    price_summary = models.FloatField()
    fat_summary = models.FloatField()
    protein_summary = models.FloatField()
    carbohydrates_summary = models.FloatField()
    cellulose_summary = models.FloatField()

    class Meta:
        ordering = ["-average_rank"]

    def __str__(self):
        return self.name


    def avg_of_given_ranks(self):
        temp = self.meals_user.aggregate(Avg('mark'))
        if temp['mark__avg'] is None:
            return 0.0
        return float(temp['mark__avg'])

    def no_of_given_ranks(self):
        # returns None if no rank is related to this instance
        return self.meals_user.aggregate(Count('mark'))



class Rank(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="meals_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals_user")
    mark = models.FloatField()

    class Meta:
        ordering = ["user_id"]

class Recommended(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="recommended")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommended")
    predicted_mark = models.FloatField(null=True)

    class Meta:
        ordering = ["user_id"]



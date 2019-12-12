from rest_framework import serializers
from BoxDiet.models import Recommended, User


class RecommendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommended
        fields = ("user_id", "meal_id", "predicted_mark")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "sex")




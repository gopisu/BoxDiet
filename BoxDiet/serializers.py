from rest_framework import serializers
from BoxDiet.models import Recommended

class RecommendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommended
        fields = ("user_id", "meal_id", "predicted_mark")

from django.http import JsonResponse
from django.views import View

from BoxDiet.models import Recommended
from BoxDiet.reccomender import predict
from RestAPI.serializers import RecommendedSerializer


# Create your views here.


class RecommendedList(View):
    def get(self, request, user_id):
        recommended = Recommended.objects.filter(user__id=user_id)
        serializer = RecommendedSerializer(recommended, many=True)
        return JsonResponse(serializer.data, safe=False)


class Prediction(View):
    def get(self, request, user_id, meal_id):
        user_id = int(user_id)
        meal_id = int(meal_id)
        predicted = predict(user_id, meal_id)
        return JsonResponse(predicted, safe=False)

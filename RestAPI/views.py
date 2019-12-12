from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from BoxDiet.models import Recommended
from RestAPI.serializers import RecommendedSerializer
# Create your views here.

class RecommendedList(View):
    def get(self, request, user_id):
        recommended = Recommended.objects.filter(user__id=user_id)
        serializer = RecommendedSerializer(recommended, many=True)
        return JsonResponse(serializer.data, safe=False)

class RecommendedList1(View):
    def get(self, request):
        recommended = Recommended.objects.filter(user__id='15343')
        serializer = RecommendedSerializer(recommended, many=True)
        return JsonResponse(serializer.data, safe=False)
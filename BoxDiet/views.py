from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.views import View

from BoxDiet.models import Meal, User, Recommended, Rank
from BoxDiet.serializers import RecommendedSerializer
from BoxDiet.utils import count, sliced_paginator, validate_int


class DashboardView(View):
    def get(self, request):
        meal_no = count(Meal)
        users_no = count(User)
        top10meals = Meal.objects.filter(average_rank__gt=4.6).order_by('-no_of_ranks')[:10]
        worst10meals = Meal.objects.filter(average_rank__lte=2.9).order_by('-no_of_ranks')[:10]
        return render(request, 'BoxDiet/dashboard.html', {'meal_no': meal_no,
                                                          'users_no': users_no, 'top10meals': top10meals,
                                                          'worst10meals': worst10meals})


class UsersView(View):

    def get(self, request, searched_name=""):
        searched_name = request.GET.get('searched_name')
        if searched_name == "" or searched_name is None:
            object_list = User.objects.order_by('-id')
            page_range, object_list = sliced_paginator(request, object_list)
        else:
            object_list = self.search_user(searched_name)
            page_range, object_list = sliced_paginator(request, object_list)
        return render(request, 'BoxDiet/user_list.html',
                      {"object_list": object_list, 'page_range': page_range, "searched_name": searched_name})

    def search_user(self, searched_name):
        try:
            searched_name = int(searched_name)
            object_list = User.objects.filter(id=searched_name)
        except ValueError:
            lower_gender = searched_name.lower()
            if lower_gender in 'kobieta':
                object_list = User.objects.filter(sex__iexact='w')
            elif lower_gender in 'mężczyzna':
                object_list = User.objects.filter(sex__iexact='m')
            else:
                object_list = User.objects.filter(sex__iexact='\\n')
        return object_list


class MealView(View):

    def get(self, request, searched_name=""):
        searched_name = request.GET.get('searched_name')
        if searched_name == "" or searched_name is None:
            object_list = Meal.objects.order_by('-average_rank').order_by('-no_of_ranks')
            page_range, object_list = sliced_paginator(request, object_list)
        else:
            object_list = self.search_meal(searched_name)
            page_range, object_list = sliced_paginator(request, object_list)
        return render(request, 'BoxDiet/meal_list.html',
                      {"object_list": object_list, 'page_range': page_range, "searched_name": searched_name})

    def search_meal(self, searched_name):
        try:
            searched_name = int(searched_name)
            object_list = Meal.objects.filter(meal_id=searched_name).order_by(
                '-average_rank').order_by('-no_of_ranks')
        except ValueError:
            object_list = Meal.objects.filter(name__icontains=searched_name).order_by(
                '-average_rank').order_by(
                '-no_of_ranks')
        return object_list


class UserDetailsView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailsView, self).get_context_data(**kwargs)
        recs = Recommended.objects.filter(user__id=self.kwargs['pk']).order_by('-predicted_mark')
        context['recs'] = recs
        return context


class UserCreateView(CreateView):
    model = User
    fields = ['sex']
    success_url = reverse_lazy('user_list')


class RankCreateView(View):
    def get(self, request):
        selected_meal = 1513
        users = User.objects.all()
        meals = Meal.objects.all()
        return render(request, "BoxDiet/rank_form.html",
                      {'users': users, 'meals': meals})

    def post(self, request):
        user_id = request.POST.get('user')
        meal_id = request.POST.get('meal')
        mark = request.POST.get('mark')
        user_id = validate_int(user_id)
        meal_id = validate_int(meal_id)
        rank = Rank.objects.create(user_id=user_id, meal_id=meal_id, mark=mark)
        form = 'BoxDiet/rank_form.html'
        return render(request, form, {'message': f'Dodano ocenę {rank.mark} dla dania {rank.meal}'})


class MealDetailsView(DetailView):
    model = Meal


class RecommendedList(View):
    def get(self, request, user_id):
        recommended = Recommended.objects.filter(user__id=user_id)
        serializer = RecommendedSerializer(recommended, many=True)
        return JsonResponse(serializer.data, safe=False)

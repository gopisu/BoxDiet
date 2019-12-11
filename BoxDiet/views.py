from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.views import View

from BoxDiet.models import Meal, User, Recommended, Rank
from BoxDiet.utils import count, sliced_paginator, validate_int


class DashboardView(View):
    def get(self, request):
        meal_no = count(Meal)
        users_no = count(User)
        top10meals = Meal.objects.order_by('-average_rank').order_by('-no_of_ranks')[:10]

        return render(request, 'BoxDiet/dashboard.html', {'meal_no': meal_no,
                                                          'users_no': users_no, 'top10meals': top10meals})


class UsersView(View):
    def get(self, request):
        object_list = User.objects.order_by('-id')
        page_range, user_list = sliced_paginator(request, object_list)
        return render(request, 'BoxDiet/user_list.html',
                      {"object_list": user_list, 'page_range': page_range})

    def post(self, request):
        searched_name = request.POST.get('searched_name')
        try:
            searched_name = int(searched_name)
            object_list = User.objects.filter(id=searched_name)
        except ValueError:
            object_list = User.objects.all()
        page_range, user_list = sliced_paginator(request, object_list)
        return render(request, 'BoxDiet/user_list.html',
                      {"object_list": user_list, 'page_range': page_range})


class MealView(View):
    def get(self, request):
        object_list = Meal.objects.order_by('-average_rank').order_by('-no_of_ranks')
        page_range, meal_list = sliced_paginator(request, object_list)
        return render(request, 'BoxDiet/meal_list.html',
                      {"object_list": meal_list, 'page_range': page_range})

    def post(self, request):
        searched_name = request.POST.get('searched_name')
        object_list = Meal.objects.filter(name__icontains=searched_name).order_by('-average_rank').order_by(
            '-no_of_ranks')
        page_range, meal_list = sliced_paginator(request, object_list)
        return render(request, 'BoxDiet/meal_list.html',
                      {"object_list": meal_list, 'page_range': page_range})


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
        users = User.objects.all()
        meals = Meal.objects.all()
        return render(request, "BoxDiet/rank_form.html", {'users': users, 'meals': meals})

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


class PopulateWithAverage(View):
    def get(self, request):
        meals = Meal.objects.all()
        for meal in meals:
            meal.average_rank = meal.avg_of_given_ranks()
            meal.save()
        return HttpResponse('dodano średnie')


class PopulateWithRanksNo(View):
    def get(self, request):
        meals = Meal.objects.all()
        for meal in meals:
            meal.no_of_ranks = meal.no_of_given_ranks()['mark__count']
            meal.save()
        return HttpResponse('dodano liczbe ocen')

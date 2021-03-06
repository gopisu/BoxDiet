from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.views.generic import DetailView, CreateView

from BoxDiet.models import Meal, User, Rank, Recommended
from BoxDiet.utils import count, sliced_paginator


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        meals_no = count(Meal)
        users_no = count(User)
        ranks_no = count(Rank)
        top10meals = Meal.objects.filter(average_rank__gt=4.6).order_by("-no_of_ranks")[
                     :10
                     ]
        worst10meals = Meal.objects.filter(average_rank__lte=2.9).order_by(
            "-no_of_ranks"
        )[:10]
        return render(
            request,
            "BoxDiet/dashboard.html",
            {
                "meals_no": meals_no,
                "ranks_no": ranks_no,
                "users_no": users_no,
                "top10meals": top10meals,
                "worst10meals": worst10meals,
            },
        )


class UsersView(LoginRequiredMixin, View):
    def get(self, request, searched_name=""):
        searched_name = request.GET.get("searched_name")
        if searched_name == "" or searched_name is None:
            object_list = User.objects.order_by("-id")
            page_range, object_list = sliced_paginator(request, object_list)
        else:
            object_list = self.search_user(searched_name)
            page_range, object_list = sliced_paginator(request, object_list)
        return render(
            request,
            "BoxDiet/user_list.html",
            {
                "object_list": object_list,
                "page_range": page_range,
                "searched_name": searched_name,
            },
        )

    def search_user(self, searched_name):
        try:
            searched_name = int(searched_name)
            object_list = User.objects.filter(id=searched_name)
        except ValueError:
            lower_gender = searched_name.lower()
            if lower_gender in "kobieta":
                object_list = User.objects.filter(sex__iexact="w")
            elif lower_gender in "mężczyzna":
                object_list = User.objects.filter(sex__iexact="m")
            else:
                object_list = User.objects.filter(sex__iexact="\\n")
        return object_list


class MealView(LoginRequiredMixin, View):
    def get(self, request, searched_name=""):
        searched_name = request.GET.get("searched_name")
        if searched_name == "" or searched_name is None:
            object_list = Meal.objects.order_by("-average_rank").order_by(
                "-no_of_ranks"
            )
            page_range, object_list = sliced_paginator(request, object_list)
        else:
            object_list = self.search_meal(searched_name)
            page_range, object_list = sliced_paginator(request, object_list)
        return render(
            request,
            "BoxDiet/meal_list.html",
            {
                "object_list": object_list,
                "page_range": page_range,
                "searched_name": searched_name,
            },
        )

    def search_meal(self, searched_name):
        try:
            searched_name = int(searched_name)
            object_list = (
                Meal.objects.filter(meal_id=searched_name)
                    .order_by("-average_rank")
                    .order_by("-no_of_ranks")
            )
        except ValueError:
            object_list = (
                Meal.objects.filter(name__icontains=searched_name)
                    .order_by("-average_rank")
                    .order_by("-no_of_ranks")
            )
        return object_list


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailsView, self).get_context_data(**kwargs)
        recs = Recommended.objects.filter(user__id=self.kwargs["pk"]).order_by(
            "meal_id"
        )
        context["recs"] = recs
        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ["sex"]
    success_url = reverse_lazy("user_list")


class RankCreateView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        meals = Meal.objects.all()
        return render(
            request, "BoxDiet/rank_form.html", {"users": users, "meals": meals}
        )

    def post(self, request):
        user_id = request.POST.get("user")
        meal_id = request.POST.get("meal")
        mark = request.POST.get("mark")
        form = "BoxDiet/rank_form.html"
        users = User.objects.all()
        meals = Meal.objects.all()

        try:
            if int(mark) in range(1, 6):
                rank = Rank.objects.create(user_id=user_id, meal_id=meal_id, mark=mark)
            else:
                message = "Nie zapisano do bazy. Wybierz ocenę od 1 do 5."
                return render(
                    request, form, {"message": message, "users": users, "meals": meals}
                )
        except:
            message = "Podaj poprawne dane!"
            return render(
                request, form, {"message": message, "users": users, "meals": meals}
            )
        return render(
            request,
            form,
            {
                "users": users,
                "meals": meals,
                "message": f"Dodano ocenę {rank.mark} dla dania {rank.meal}",
            },
        )


class MealDetailsView(LoginRequiredMixin, DetailView):
    model = Meal


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

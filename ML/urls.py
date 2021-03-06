"""ML URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from BoxDiet.views import (
    DashboardView,
    UsersView,
    UserDetailsView,
    MealView,
    MealDetailsView,
    UserCreateView,
    RankCreateView,
    SignUp,
)

urlpatterns = [
    path("admin/", admin.site.urls, name="test"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("user-list/", UsersView.as_view(), name="user_list"),
    path("meal-list/", MealView.as_view(), name="meal_list"),
    path("user-details/<int:pk>", UserDetailsView.as_view(), name="user_detail"),
    path("meal-details/<int:pk>", MealDetailsView.as_view(), name="meal_detail"),
    path("user-create/", UserCreateView.as_view(), name="user_create"),
    path("rank-create/", RankCreateView.as_view(), name="rank_create"),
    path("API/", include("RestAPI.urls")),
    path("box/", include("django.contrib.auth.urls")),
    path("signup/", SignUp.as_view(), name="signup"),
]

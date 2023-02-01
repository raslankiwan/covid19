"""covid19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from rest_framework import routers

from covid19.views.auth.login_view import login_view
from covid19.views.auth.logout_view import logout_view
from covid19.views.auth.register_view import register_view
from covid19.views.api.add_country import add_country
from covid19.views.api.user_statistics import user_statistics
from covid19.views.api.death_percentage import death_percentage
from covid19.views.api.top_countries import top_countries
from covid19.views.api.fill_country_stats import fill_country_stats


router = routers.DefaultRouter()
urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_view),
    path("login/", login_view),
    path("logout/", logout_view),
    path("add-country/", add_country),
    path("user-statistics/", user_statistics),
    path("death-percentage/", death_percentage),
    path("top-countries/", top_countries),
    path("fill-stats/", fill_country_stats),
]

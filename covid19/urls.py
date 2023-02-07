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

from covid19.views.api.add_country import AddCountryView
from covid19.views.api.death_percentage import DeathPercentage
from covid19.views.api.top_countries import TopCountries
from covid19.views.auth.login_view import Login
from covid19.views.auth.register_view import Register

router = routers.DefaultRouter()
urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", Register.as_view()),
    path("login/", Login.as_view()),
    path("add-country/", AddCountryView.as_view()),
    path("death-percentage/", DeathPercentage.as_view()),
    path("top-countries/", TopCountries.as_view()),
]

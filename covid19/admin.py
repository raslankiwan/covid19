from django.contrib import admin

from .models import Country, CountryDailyStats

admin.site.register(Country)
admin.site.register(CountryDailyStats)

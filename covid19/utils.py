import requests

from covid19.models.country_daily_stats import CountryDailyStats
from covid19.models.country import Country


def fill_stats_by_country(country_name):
    country_data = requests.get(
        f'https://api.covid19api.com/country/{country_name}').json()
    try:
        country = Country.objects.get(name=country_name)
    except Country.DoesNotExist:
        country = Country.objects.create(name=country_name)
    for item in country_data:
        try:
            daily_stats = CountryDailyStats.objects.get(
                country=country, date=item["Date"])
        except CountryDailyStats.DoesNotExist:
            CountryDailyStats.objects.create(date=item["Date"], country=country, confirmed=item["Confirmed"],
                                             deaths=item["Deaths"], recovered=item["Recovered"], active=item["Active"])


def fill_all_countries():
    countries = Country.objects.all()
    for country in countries:
        country_data = requests.get(
            f'https://api.covid19api.com/country/{country.name}').json()
        for item in country_data:
            try:
                daily_stats = CountryDailyStats.objects.get(
                    country=country, date=item["Date"])
            except CountryDailyStats.DoesNotExist:
                CountryDailyStats.objects.create(date=item["Date"], country=country, confirmed=item["Confirmed"],
                                                 deaths=item["Deaths"], recovered=item["Recovered"], active=item["Active"])

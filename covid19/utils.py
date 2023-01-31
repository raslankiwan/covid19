import requests

from covid19.models.country_daily_stats import CountryDailyStats


def fill_stats_by_country(country):
    country_data = requests.get(
        f'https://api.covid19api.com/country/{country}').json()
    for item in country_data:
        try:
            daily_stats = CountryDailyStats.objects.get(
                country=country, date=item["Date"])
        except CountryDailyStats.DoesNotExist:
            CountryDailyStats.objects.create(date=item["Date"], country=country, confirmed=item["Confirmed"],
                                             deaths=item["Deaths"], recovered=item["Recovered"], active=item["Active"])

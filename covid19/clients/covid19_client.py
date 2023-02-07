import logging
from datetime import datetime, timedelta

import requests

from covid19.models import Country, CountryDailyStats

logger = logging.getLogger('django')


class Covid19Client():

    def create_today_result(self, today_data, yesterday_data, country):

        date = datetime.fromisoformat(today_data["Date"])
        result = CountryDailyStats.objects.create(
            date=date.strftime("%Y-%m-%d"),
            country=country,
            confirmed=abs(today_data["Confirmed"] -
                          yesterday_data["Confirmed"]),
            deaths=abs(today_data["Deaths"] - yesterday_data["Deaths"]),
            recovered=abs(today_data["Recovered"] -
                          yesterday_data["Recovered"]),
            active=today_data["Active"])
        return result

    def fill_today_for_all(self):
        yesterday_datetime = datetime.now() - timedelta(days=1)
        yesterday_datetime = yesterday_datetime.strftime("%Y-%m-%dT00:00:00Z")
        today_datetime = datetime.now().strftime("%Y-%m-%dT00:00:00Z")

        countries = Country.objects.all()

        for country in countries:
            try:
                country_data = requests.get(
                    f'https://api.covid19api.com/country/{country.name}?from={yesterday_datetime}&to={today_datetime}').json()
            except Exception as error:
                logger.error(
                    f"Error retrieving info for {country.name}, Error: {error}")
                continue
            self.create_today_result(
                today_data=country_data[1], yesterday_data=country_data[0], country=country)

    def fill_stats_by_country(self, country_name):
        try:
            country_data = requests.get(
                f'https://api.covid19api.com/country/{country_name}').json()
            try:
                country = Country.objects.get(name=country_name)
            except Country.DoesNotExist:
                country = Country.objects.create(name=country_name)
            for index in range(1, len(country_data)):
                self.create_today_result(
                    today_data=country_data[index], yesterday_data=country_data[index - 1], country=country)
        except Exception as error:
            logger.error(
                f"Unable to get results for {country_name}, Error: {error}")

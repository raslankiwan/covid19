# pylint: disable=import-error
import logging

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from covid19.models.country_daily_stats import CountryDailyStats

logger = logging.getLogger('django')


@csrf_exempt
@api_view(['POST'])
def fill_country_stats(request):

    country = request.data.get('country', '')
    logger.info(f'Getting daily stats for {country}')

    country_data = requests.get(
        f'https://api.covid19api.com/country/{country}').json()

    for item in country_data:
        try:
            daily_stats = CountryDailyStats.objects.get(
                country=country, date=item["Date"])
        except CountryDailyStats.DoesNotExist:
            CountryDailyStats.objects.create(date=item["Date"],
                                             country=country, confirmed=item["Confirmed"],
                                             deaths=item["Deaths"], recovered=item["Recovered"],
                                             active=item["Active"])

    return JsonResponse({'success': True})

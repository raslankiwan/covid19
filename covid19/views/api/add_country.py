import json
import logging
import requests

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from covid19.models.user_setting import UserSetting
from covid19.models.country_daily_stats import CountryDailyStats

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
def add_country(request):
    user_id = request.user.id
    request_body = json.loads(request.body.decode("utf-8"))

    countries = request_body['countries']

    for country in countries:
        country_data = requests.get(
            f'https://api.covid19api.com/country/{country}').json()
        for item in country_data:
            try:
                daily_stats = CountryDailyStats.objects.get(
                    country=country, date=item["Date"])
            except CountryDailyStats.DoesNotExist:
                CountryDailyStats.objects.create(date=item["Date"], country=country, confirmed=item["Confirmed"],
                                                 deaths=item["Deaths"], recovered=item["Recovered"], active=item["Active"])

    try:
        user_setting = UserSetting.objects.get(user_id=user_id)
    except UserSetting.DoesNotExist:
        user_setting = None

    if user_setting is None:
        user_setting = UserSetting.objects.create(
            user_id=request.user)
        user_setting.set_countries(countries)
        user_setting.save()
    else:
        user_countries = []

        if user_setting.countries:
            user_countries = user_setting.get_countries()
        user_setting.countries = list(set(user_countries) | set(countries))
        user_setting.save()
    return JsonResponse({'user_setting': model_to_dict(user_setting)})

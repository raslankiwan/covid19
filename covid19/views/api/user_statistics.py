import logging

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from covid19.models.user_setting import UserSetting

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['GET'])
def user_statistics(request):
    user_id = request.user.id
    start_date = request.GET.get('startDate', '')
    end_date = request.GET.get('endDate', '')

    user_setting = UserSetting.objects.get(user_id=user_id)
    result = {}
    countries = user_setting.get_countries()
    for country in countries:
        r = requests.get(
            f'https://api.covid19api.com/country/{country}?from={start_date}&to={end_date}').json()
        result[country] = r

    return JsonResponse({'result': result})

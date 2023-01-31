# pylint: disable=import-error
import logging

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from covid19.models.country_daily_stats import CountryDailyStats
from covid19.models.user_setting import UserSetting

logger = logging.getLogger('django')


@csrf_exempt
@api_view(['GET'])
def user_statistics(request):
    user_id = request.user.id

    logger.info(f'Getting countries summary for user {user_id}')

    user_setting = UserSetting.objects.get(user_id=user_id)
    countries = user_setting.get_countries()

    all_country_stats = []
    for country in countries:
        country_stats = CountryDailyStats.objects.filter(
            country=country).latest('date')
        all_country_stats.append(model_to_dict(country_stats))

    return JsonResponse({'result': all_country_stats})

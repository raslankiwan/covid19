import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.core import serializers
from django.forms.models import model_to_dict

from covid19.models.country_daily_stats import CountryDailyStats
from covid19.models.user_setting import UserSetting

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['GET'])
def top_countries(request):
    user_id = request.user.id
    status = request.GET.get('status', '')
    limit = int(request.GET.get('limit', 3))

    user_setting = UserSetting.objects.get(user_id=user_id)
    countries = user_setting.get_countries()
    # top3 = CountryDailyStats.objects.filter(country in countries).latest()
    all_stats = []
    for country in countries:
        country_stats = CountryDailyStats.objects.filter(
            country=country).latest('date')
        all_stats.append(model_to_dict(country_stats))

    all_stats.sort(key=lambda x: x[status], reverse=True)

    # result = json.loads(serializers.serialize('json', all_stats[:3]))
    return JsonResponse({'result': all_stats[:limit]})

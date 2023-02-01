import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from covid19.models.country_daily_stats import CountryDailyStats  # pylint: disable=import-error

logger = logging.getLogger('django')


@csrf_exempt
@api_view(['GET'])
def death_percentage(request):
    country = request.GET.get('country', '')
    logger.info(f'Getting deaths to confirmed ratio for {country}')

    try:
        last_day_stats = CountryDailyStats.objects.filter(
            country=country).latest('date')
    except CountryDailyStats.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if last_day_stats is not None:
        death_to_confirmed_ratio = (
            last_day_stats.deaths / last_day_stats.confirmed) * 100
        return JsonResponse({'result': death_to_confirmed_ratio})

    else:
        return JsonResponse({'error': 'Error getting percentage'})

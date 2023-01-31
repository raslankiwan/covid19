# pylint: disable=import-error
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from covid19.utils import fill_stats_by_country

logger = logging.getLogger('django')


@csrf_exempt
@api_view(['POST'])
def fill_country_stats(request):

    country = request.data.get('country', '')
    logger.info(f'Filling daily stats for {country}')
    fill_stats_by_country(country)

    return JsonResponse({'success': True})

# pylint: disable=import-error
import logging

from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from covid19.models import Country
from covid19.serializers import TopCountriesSerializer

logger = logging.getLogger('django')


class TopCountries(APIView):

    def get(self, request):
        user_id = request.user.id
        status = request.GET.get('status', '')
        limit = int(request.GET.get('limit', 3))

        logger.info(f'Getting top {limit} countries for user {user_id}')

        countries = Country.objects.filter(users__id=user_id).annotate(total_deaths=Sum(
            "countrydailystats__deaths"), total_confirmed=Sum("countrydailystats__confirmed")) .order_by('-total_'+status)[:limit]
        all_country_stats = TopCountriesSerializer(countries, many=True)

        return Response(all_country_stats.data)

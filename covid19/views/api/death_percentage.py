# pylint: disable=import-error
import logging

from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from covid19.models import Country, CountryDailyStats

logger = logging.getLogger('django')


class DeathPercentage(APIView):

    def get(self, request):
        country = request.GET.get('country', '')
        logger.info(f'Getting deaths to confirmed ratio for {country}')

        try:
            try:
                country = Country.objects.get(name=country)
                if not request.user in country.users.all():
                    return Response({'error': 'user is not subscribed to this country'})

            except Country.DoesNotExist:
                return Response({'error': 'Country not found'})

            some_result = CountryDailyStats.objects.aggregate(
                Sum('deaths'), Sum('confirmed'), )

            death_to_confirmed_ratio = (
                some_result['deaths__sum'] / some_result['confirmed__sum']) * 100
            return Response({'result': death_to_confirmed_ratio})

        except CountryDailyStats.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

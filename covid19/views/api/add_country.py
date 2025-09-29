# pylint: disable=import-error
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from covid19.clients.covid19_client import Covid19Client
from covid19.models import Country
from covid19.serializers import CountrySerializer

logger = logging.getLogger(__name__)


class AddCountryView(APIView):

    def post(self, request):
        countries = request.data.get('countries', [])

        for country_name in countries:
            try:
                country_instance = Country.objects.get(name=country_name)

                country = CountrySerializer(
                    country_instance,
                    data={"name": country_name}, context={"user": request.user})

                if country.is_valid():
                    country.save()
                else:
                    return Response(country.errors, status=status.HTTP_400_BAD_REQUEST)

            except Country.DoesNotExist:
                Covid19Client().fill_stats_by_country(country_name)
                country = CountrySerializer(
                    data={"name": country_name}, context={"user": request.user})
                if country.is_valid():
                    country.save()
                else:
                    return Response(country.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

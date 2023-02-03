# pylint: disable=import-error
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from covid19.models.user_setting import UserSetting
from covid19.models.country import Country
from covid19.utils import fill_stats_by_country

logger = logging.getLogger(__name__)


class AddCountryView(APIView):

    @csrf_exempt
    def post(self, request):
        user_id = request.user.id

        countries = request.data.get('countries', [])

        try:
            user_setting = UserSetting.objects.get(user_id=user_id)
        except UserSetting.DoesNotExist:
            user_setting = UserSetting.objects.create(user_id=request.user)

        for country in countries:
            try:
                country_model = Country.objects.get(name=country)
            except Country.DoesNotExist:
                country_model = Country.objects.create(name=country)
                fill_stats_by_country(country)
            user_setting.countries.add(country_model)
            user_setting.save()
        return JsonResponse({'result': 'success'} )

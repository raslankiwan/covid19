# pylint: disable=import-error
import json
import logging

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from covid19.models.user_setting import UserSetting
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
            user_setting = None

        if user_setting is None:
            for country in countries:
                fill_stats_by_country(country)

            user_setting = UserSetting.objects.create(
                user_id=request.user, countries=json.dumps(countries))
        else:
            for country in countries:
                user_setting.add_country(country)
            user_setting.save()
        return JsonResponse({'user_setting': model_to_dict(user_setting)})

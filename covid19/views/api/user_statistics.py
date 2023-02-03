# pylint: disable=import-error
import logging
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from covid19.models.country_daily_stats import CountryDailyStats
from covid19.models.user_setting import UserSetting

logger = logging.getLogger('django')


class UserStats(APIView):

    @csrf_exempt
    def get(self, request):
        user_id = request.user.id
        date = request.GET.get('date', '')

        date_before = datetime.fromisoformat(date) - timedelta(days=1)
        date_before = date_before.strftime("%Y-%m-%dT00:00:00Z")
        date_str = datetime.fromisoformat(date).strftime("%Y-%m-%dT00:00:00Z")
        logger.info(f'Getting countries summary for user {user_id}')

        user_setting = UserSetting.objects.get(user_id=user_id)
        countries = user_setting.countries.all()

        all_country_stats = []
        for country in countries:
            day_before_stats = CountryDailyStats.objects.get(
                country=country.id, date=date_before)
            country_stats = CountryDailyStats.objects.get(
                country=country.id, date=date_str)
            all_country_stats.append({
                "country": country.name,
                "date": date_str,
                "confirmed": country_stats.confirmed - day_before_stats.confirmed,
                "deaths": country_stats.deaths - day_before_stats.deaths,
                "recovered": country_stats.recovered - day_before_stats.recovered,
                "active": country_stats.active - day_before_stats.active
            })

        return JsonResponse({'result': all_country_stats})

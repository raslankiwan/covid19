import ast
import json

from django.contrib.auth.models import User  # pylint: disable=imported-auth-user
from django.db import models
from covid19.utils import fill_stats_by_country


class UserSetting(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    countries = models.TextField(max_length=200)

    def set_countries(self, lst):
        self.countries = json.dumps(lst)

    def get_countries(self):
        return ast.literal_eval(self.countries)

    def add_country(self, country):
        user_countries = self.get_countries()
        if country not in user_countries:
            fill_stats_by_country(country)
            user_countries.append(country)
            self.set_countries(user_countries)

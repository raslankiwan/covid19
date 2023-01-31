import ast
import json

from django.contrib.auth.models import User
from django.db import models


class UserSetting(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    countries = models.TextField(max_length=200)

    def set_countries(self, lst):
        ast.dump(node)
        self.countries = json.dumps(lst)

    def get_countries(self):
        return ast.literal_eval(self.countries)

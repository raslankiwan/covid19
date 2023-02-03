from django.contrib.auth.models import User  # pylint: disable=imported-auth-user
from django.db import models

from covid19.models.country import Country


class UserSetting(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    countries = models.ManyToManyField(Country)

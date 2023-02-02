from django.db import models
from covid19.models.country import Country


class CountryDailyStats(models.Model):
    date = models.DateTimeField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    confirmed = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    active = models.IntegerField()

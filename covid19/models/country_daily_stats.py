from django.db import models


class CountryDailyStats(models.Model):
    date = models.DateTimeField()
    country = models.CharField(max_length=50)
    confirmed = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    active = models.IntegerField()

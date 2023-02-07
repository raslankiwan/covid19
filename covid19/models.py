from django.contrib.auth.models import User  # pylint: disable=imported-auth-user
from django.db import models
from django.db.models import UniqueConstraint


class Country(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class CountryDailyStats(models.Model):
    date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    confirmed = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    recovered = models.PositiveIntegerField()
    active = models.PositiveIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                'date',
                'country',
                name='date_country_unique',
            ),
        ]

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=250)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"


class Subscription(models.Model):
    PERIOD_CHOICES = [
        (1, '1 hour'),
        (3, '3 hours'),
        (6, '6 hours'),
        (12, '12 hours'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    period = models.IntegerField(choices=PERIOD_CHOICES)
    active = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def __str__(self):
        return f"{self.user} - {self.city.name} ({self.period} hours)"


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    country = models.CharField(max_length=250)
    temperature_celsius = models.FloatField()
    humidity = models.IntegerField(default=0)
    weather = models.TextField(blank=True)
    icon = models.CharField(max_length=250)
    updated = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.city}-{self.country}-{self.temperature_celsius}"

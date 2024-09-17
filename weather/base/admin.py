from django.contrib import admin
from .models import Weather, City, Subscription

admin.site.register(Weather)
admin.site.register(City)
admin.site.register(Subscription)

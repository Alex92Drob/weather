import requests
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse, HttpResponseServerError

from .models import Weather, City, Subscription
from weather.settings import WEATHER_API_KEY
from .serializers import (
    CitySerializer, WeatherSerializer, SubscriptionSerializer,
    UserRegistrationSerializer, MyTokenObtainPairSerializer
)


#Get data from WeatherAPI and save to db
def get_weather(city_name):
    api_key = WEATHER_API_KEY
    url = 'https://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'
    try:
        response = requests.get(url.format(api_key, city_name))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as http_err:
        # HTTP error handling
        return HttpResponseServerError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        # Handling other request errors
        return HttpResponseServerError(f"Error occurred: {req_err}")
    if data:
        # Get or create a city record
        city, created = City.objects.get_or_create(name=city_name)
        # Getting weather data
        weather_info = {
            'city': data['location']['name'],
            'country': data['location']['country'],
            'temperature_celsius': data['current']['temp_c'],
            'humidity': data['current']['humidity'],
            'weather': data['current']['condition']['text'],
            'icon_url': "https:" + data['current']['condition']['icon'],
        }
        # Store weather data in the database
        weather_data, created = Weather.objects.update_or_create(
            city=city,
            defaults={
                'country': weather_info['country'],
                'temperature_celsius': weather_info['temperature_celsius'],
                'humidity': weather_info['humidity'],
                'weather': weather_info['weather'],
                'icon': weather_info['icon_url']
            }
        )
        # Transfer data to the template
        return JsonResponse(weather_info)
    else:
        # If there is no data, return an error
        return HttpResponseServerError("Error: Unable to fetch weather data")


class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated,)


class WeatherList(generics.ListCreateAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        subscribed_city_id = City.objects.filter(
            subscription__user=self.request.user
        ).values_list('id', flat=True)
        return Weather.objects.filter(city_id__in=subscribed_city_id)


class SubscriptionList(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

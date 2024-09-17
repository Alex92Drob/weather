"""
URL configuration for weather project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from base.views import (
    RegisterView, MyObtainTokenPairView, CityList, WeatherList, SubscriptionList, get_weather, SubscriptionDetail
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('cities/', CityList.as_view(), name='cities'),
    path('weather/', WeatherList.as_view(), name='weather'),
    path('subscription/', SubscriptionList.as_view(), name='subscription'),
    path('subscription_detail/<int:pk>/', SubscriptionDetail.as_view(), name='subscription_detail'),
    path('get_weather/', get_weather, name='get_weather'),
]

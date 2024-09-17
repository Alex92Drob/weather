import time
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Subscription, Weather, City
from .views import get_weather


@shared_task
def weather_data_to_db():
    for city in City.objects.values_list('name', flat=True).distinct():
        get_weather(city)
        time.sleep(5)
        print(f'*** {city} weather data added ***')


@shared_task
def send_weather_email(subscription_id):
    try:
        # Fetch subscription
        subscription = Subscription.objects.get(id=subscription_id)
        user = subscription.user
        city = subscription.city
        period = subscription.period

        # Get weather data for the city
        weather_data = Weather.objects.filter(city_id=city).last()

        # Create the email content
        subject = f"Weather update for {city.name}"
        message = f"Hello, {user.username}!\n\n" \
                  f"Here is the latest weather update for {city.name}:\n" \
                  f'weather: {weather_data.weather}\n' \
                  f'temp: {weather_data.temperature_celsius}\n' \
                  f'humidity: {weather_data.humidity}\n'

        # Send the email
        send_mail(
            subject,
            message,
            'weather_service@example.com',  # Your email or SMTP settings
            [user.email],
            fail_silently=False,
        )

    except Subscription.DoesNotExist:
        print(f"Subscription with ID {subscription_id} not found")
    except Exception as e:
        print(f"Error while sending email: {e}")


@shared_task
def check_subscriptions_and_send_emails():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        time_since_last_run = timezone.now() - subscription.last_run_at
        hours_passed = time_since_last_run.total_seconds() // 3600
        print(f"Checking subscription {subscription}: Last run {subscription.last_run_at}, Hours passed: {hours_passed}")
        if hours_passed >= subscription.period:
            send_weather_email.delay_on_commit(subscription.id)
            subscription.last_run_at = timezone.now()
            subscription.save()
            print(f"Email send to {subscription.user.email} for city {subscription.city.name}")

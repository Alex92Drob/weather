import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')
app = Celery('weather')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'record-weather-information-every-hour': {
        'task': 'wapp.tasks.weather_data_to_db',
        'schedule': 3600.0,
    },
    'check_subscriptions_and_send_emails': {
        'task': 'wapp.tasks.check_subscriptions_and_send_emails',
        'schedule': 1800.0,
    },
}
app.conf.timezone = 'UTC'
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")

# Конфигурация Celery
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Использование DatabaseScheduler
app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

# Периодические задачи (лучше перенести в settings.py)
app.conf.beat_schedule = {
    "check-mailings-every-minute": {
        "task": "config.celery.check_mailings",
        "schedule": 60.0,  # Каждые 60 секунд
    },
}

@app.task
def check_mailings():
    from mailing.models import Mailing
    from django.utils import timezone

    now = timezone.now()
    mailings = Mailing.objects.filter(
        status__in=["created", "started"],
        start_time__lte=now,
        end_time__gte=now
    )

    for mailing in mailings:
        mailing.send_to_recipients()
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60.0,  # Каждые 60 секунд
        check_mailings.s(),
        name='check_mailings'
    )


@app.task
def check_mailings():
    from mailing.models import Mailing
    from django.utils import timezone

    now = timezone.now()
    mailings = Mailing.objects.filter(
        status__in=['created', 'started'],
        start_time__lte=now,
        end_time__gte=now
    )

    for mailing in mailings:
        mailing.send_to_recipients()

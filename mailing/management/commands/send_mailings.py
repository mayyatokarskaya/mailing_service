from django.core.management.base import BaseCommand
from mailing.models import Mailing
from django.utils import timezone


class Command(BaseCommand):
    help = 'Отправляет все активные рассылки'

    def handle(self, *args, **options):
        now = timezone.now()

        # рассылки, которые нужно отправить:
        # - статус 'started' или 'created'
        # - текущее время между start_time и end_time
        mailings = Mailing.objects.filter(
            status__in=['created', 'started'],
            start_time__lte=now,
            end_time__gte=now
        )

        for mailing in mailings:
            self.stdout.write(f"Отправка рассылки #{mailing.id}...")
            mailing.send_to_recipients()
            self.stdout.write(f"Рассылка #{mailing.id} отправлена!")

        self.stdout.write("Готово!")
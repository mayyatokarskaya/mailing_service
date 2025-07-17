from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='recipients')

    class Meta:
        permissions = [
            ('view_all_recipients', 'Can view all recipients'),
        ]

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    mailing = models.ForeignKey(
        'Mailing',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='messages'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    class Meta:
        permissions = [
            ('view_all_messages', 'Can view all messages'),
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("completed", "Завершена"),
        ("created", "Создана"),
        ("started", "Запущена"),
    ]

    class Meta:
        permissions = [
            ('view_all_mailings', 'Can view all mailings'),
        ]

    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус")
    message = models.ForeignKey(
        "Message",
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name='mailings'
    )
    recipients = models.ManyToManyField("Recipient", verbose_name="Получатели")
    owner = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='mailings'
    )

    def __str__(self):
        return f"Рассылка {self.id} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        """Автоматически обновляет статус при сохранении."""

        if self.start_time >= self.end_time:
            raise ValueError("Дата и время начала должны быть раньше даты и времени окончания.")

        now = timezone.now()

        if self.status != "completed" and now > self.end_time:
            self.status = "completed"

        if self.status == "created" and self.start_time <= now <= self.end_time:
            self.status = "started"

        super().save(*args, **kwargs)

    def send_to_recipients(self):
        """Отправляет письма всем получателям рассылки."""
        if self.status != "started":
            self.status = "started"
            self.save()

        for recipient in self.recipients.all():
            try:
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email="noreply@yourdomain.com",
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(mailing=self, status="success", server_response="200 OK")
            except Exception as e:
                MailingAttempt.objects.create(mailing=self, status="failed", server_response=str(e))

        if timezone.now() > self.end_time:
            self.status = "completed"
            self.save()

    def get_stats(self):
        return {
            'success': self.attempts.filter(status='success').count(),
            'failed': self.attempts.filter(status='failed').count(),
            'total': self.attempts.count()
        }


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Попытка {self.id} ({self.get_status_display()})"

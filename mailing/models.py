from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.template.loader import render_to_string


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)

    def __str__(self):
        return f"Рассылка {self.id} ({self.get_status_display()})"

    def send_to_recipients(self):
        if self.status != 'started':
            self.status = 'started'
            self.save()

        for recipient in self.recipients.all():
            try:
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email='noreply@yourdomain.com',
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=self,
                    status='success',
                    server_response='200 OK'
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=self,
                    status='failed',
                    server_response=str(e)
                )

        if timezone.now() > self.end_time:
            self.status = 'completed'
            self.save()


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Попытка {self.id} ({self.get_status_display()})"
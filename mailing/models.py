from django.db import models


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
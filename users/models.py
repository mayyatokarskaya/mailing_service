from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def send_verification_email(self):
        send_mail(
            'Подтвердите email',
            f'Перейдите по ссылке: http://ваш-сайт/verify/{self.pk}/',
            DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )

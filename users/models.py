from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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

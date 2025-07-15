from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Отправка email с подтверждением (заглушка)
            send_mail(
                'Подтвердите email',
                f'Перейдите по ссылке для подтверждения: http://127.0.0.1:8000/users/verify/{user.pk}/',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def verify_email(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        user.is_verified = True
        user.save()
        messages.success(request, 'Email подтвержден! Теперь вы можете войти.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')

    return redirect('login')


class VerifiedLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_verified:
            messages.error(self.request, 'Подтвердите email перед входом.')
            return redirect('login')
        return super().form_valid(form)

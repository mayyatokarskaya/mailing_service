from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import CustomUserCreationForm
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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


class ManagerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UserListView(ManagerRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'


@login_required
def toggle_block_user(request, user_id):
    if not request.user.is_staff:
        raise PermissionDenied

    user = get_object_or_404(CustomUser, pk=user_id)
    user.is_active = not user.is_active
    user.save()

    messages.success(request, f'Пользователь {"заблокирован" if not user.is_active else "разблокирован"}.')

    return redirect('user_list')

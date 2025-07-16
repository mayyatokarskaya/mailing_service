from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page

from mailing.models import Mailing
from django.contrib import messages
from .mixins import OwnerRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Recipient


def send_mailing_view(request, mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    mailing.send_to_recipients()
    messages.success(request, f"Рассылка #{mailing_id} отправлена!")
    return redirect("admin:mailing_mailing_changelist")


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='started').count()
    unique_recipients = Recipient.objects.count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients
    }

    return render(request, 'mailing/home.html', context)


@login_required
def stats(request):
    mailings = Mailing.objects.filter(owner=request.user)
    stats = [m.get_stats() for m in mailings]
    return render(request, 'mailing/stats.html', {'stats': stats})


class MailingUpdateView(OwnerRequiredMixin, UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time']


@cache_page(60 * 15)
def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'mailing/mailing_list.html', {'mailings': mailings})


def home(request):
    total_mailings = Mailing.objects.count()  # всего рассылок
    active_mailings = Mailing.objects.filter(status='started').count()  # активных рассылок
    unique_recipients = Recipient.objects.count()  # всего получателей

    return render(request, 'mailing/home.html', {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients
    })


class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = 'mailing/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('recipient_list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = 'mailing/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('recipient_list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')


class ManagerRecipientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Recipient
    template_name = 'mailing/manager_recipient_list.html'  # укажем шаблон
    context_object_name = 'recipients'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from django.views.generic import UpdateView

from mailing.models import Mailing, Recipient
from django.contrib import messages
from .mixins import OwnerRequiredMixin


def send_mailing_view(request, mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    mailing.send_to_recipients()
    messages.success(request, f"Рассылка #{mailing_id} отправлена!")
    return redirect("admin:mailing_mailing_changelist")


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
    return render(request, 'mailing/list.html', {'mailings': mailings})


def home(request):
    total_mailings = Mailing.objects.count()  # всего рассылок
    active_mailings = Mailing.objects.filter(status='started').count()  # активных рассылок
    unique_recipients = Recipient.objects.count()  # всего получателей

    return render(request, 'mailing/home.html', {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients
    })

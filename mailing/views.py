from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from django.views.generic import UpdateView

from mailing.models import Mailing
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

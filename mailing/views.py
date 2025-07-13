from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from mailing.models import Mailing
from django.contrib import messages


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
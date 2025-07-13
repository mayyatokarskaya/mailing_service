from django.shortcuts import redirect
from mailing.models import Mailing
from django.contrib import messages


def send_mailing_view(request, mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    mailing.send_to_recipients()
    messages.success(request, f"Рассылка #{mailing_id} отправлена!")
    return redirect("admin:mailing_mailing_changelist")

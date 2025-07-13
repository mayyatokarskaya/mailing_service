from django.contrib import admin
from django.urls import path
from mailing.views import send_mailing_view

urlpatterns = [
    path('admin/mailing/mailing/<int:mailing_id>/send/', send_mailing_view, name='send_mailing'),
    path('admin/', admin.site.urls),
]

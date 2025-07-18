from django.contrib import admin
from django.urls import path, include

from mailing import views
from mailing.views import send_mailing_view, MailingAttemptListView, MailingReportView
from mailing.views import home
from mailing.views import (
    RecipientListView,
    RecipientDetailView,
    RecipientCreateView,
    RecipientUpdateView,
    RecipientDeleteView,
)

urlpatterns = [
    path("", home, name="home"),
    path("admin/mailing/mailing/<int:mailing_id>/send/", send_mailing_view, name="send_mailing"),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("mailings/", views.mailing_list, name="mailing_list"),
    path("users/", include("users.urls")),
    path("manager/recipients/", views.ManagerRecipientListView.as_view(), name="manager_recipient_list"),
    path("", include("mailing.urls")),
    path("attempts/", MailingAttemptListView.as_view(), name="attempt_list"),
    path("report/", MailingReportView.as_view(), name="mailing_report"),
]


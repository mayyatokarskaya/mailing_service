from django.urls import path
from .views import (
    RecipientListView, RecipientDetailView, RecipientCreateView,
    RecipientUpdateView, RecipientDeleteView,

    MailingListView, MailingDetailView, MailingCreateView,
    MailingUpdateView, MailingDeleteView
)

urlpatterns = [
    # Recipient
    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    # Mailing
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]

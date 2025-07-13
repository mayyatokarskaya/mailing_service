from django.urls import path
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse

from .models import Recipient, Message, Mailing, MailingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')
    list_filter = ('email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    search_fields = ('subject',)


class MailingAttemptInline(admin.TabularInline):  # или StackedInline
    model = MailingAttempt
    extra = 0
    readonly_fields = ('attempt_time', 'status', 'server_response')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'status', 'send_button')
    list_filter = ('status', 'start_time')
    actions = ['send_selected_mailings']
    inlines = [MailingAttemptInline]  # Добавляем inline для попыток

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/send/',
                self.admin_site.admin_view(self.send_mailing_view),
                name='send_mailing'
            ),
        ]
        return custom_urls + urls

    def send_mailing_view(self, request, object_id):
        mailing = self.get_object(request, object_id)
        mailing.send_to_recipients()
        self.message_user(request, f"Рассылка #{mailing.id} отправлена!")
        return HttpResponseRedirect(reverse('admin:mailing_mailing_changelist'))

    def send_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Отправить</a>',
            reverse('admin:send_mailing', args=[obj.id])
        )

    send_button.short_description = "Действие"

    def send_selected_mailings(self, request, queryset):
        for mailing in queryset:
            mailing.send_to_recipients()
        self.message_user(request, "Рассылки отправлены!")

    send_selected_mailings.short_description = "Отправить выбранные рассылки"


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_time', 'status')
    list_filter = ('status', 'attempt_time')
    readonly_fields = ('attempt_time', 'status', 'server_response', 'mailing')
    search_fields = ('mailing__message__subject',)

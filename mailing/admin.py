from django.contrib import admin
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
    list_display = ('id', 'start_time', 'end_time', 'status', 'message')
    list_filter = ('status', 'start_time')
    search_fields = ('message__subject',)
    filter_horizontal = ('recipients',)
    inlines = [MailingAttemptInline]
    actions = ['send_mailings']

    def send_mailings(self, request, queryset):
        for mailing in queryset:
            mailing.send_to_recipients()
        self.message_user(request, "Выбранные рассылки отправлены")
    send_mailings.short_description = "Отправить выбранные рассылки"

@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_time', 'status')
    list_filter = ('status', 'attempt_time')
    readonly_fields = ('attempt_time', 'status', 'server_response', 'mailing')
    search_fields = ('mailing__message__subject',)
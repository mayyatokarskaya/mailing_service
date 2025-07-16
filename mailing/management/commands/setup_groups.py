from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" и назначает права'

    def handle(self, *args, **kwargs):
        manager_group, created = Group.objects.get_or_create(name='manager')

        permissions = Permission.objects.filter(
            codename__in=[
                'view_all_mailings',
                'view_all_recipients',
                'view_all_messages',
            ]
        )
        manager_group.permissions.set(permissions)
        manager_group.save()

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует'))


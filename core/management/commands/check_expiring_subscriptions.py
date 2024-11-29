from django.core.management.base import BaseCommand
from core.tasks import check_subscription_expiry

class Command(BaseCommand):
    help = 'Checks for expiring subscriptions and creates notifications'

    def handle(self, *args, **kwargs):
        check_subscription_expiry()
        self.stdout.write(self.style.SUCCESS('Successfully checked expiring subscriptions'))


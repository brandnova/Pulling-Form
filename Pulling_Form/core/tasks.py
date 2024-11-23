from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import UserProfile

@shared_task
def send_subscription_expiry_reminders():
    # Get all active subscriptions expiring in 5 days
    expiry_date = timezone.now().date() + timezone.timedelta(days=5)
    expiring_profiles = UserProfile.objects.filter(
        is_active=True,
        subscription_expiry_date=expiry_date
    )

    for profile in expiring_profiles:
        send_mail(
            'Subscription Expiry Reminder',
            f'Your subscription will expire on {profile.subscription_expiry_date}. Please renew to continue using our services.',
            settings.DEFAULT_FROM_EMAIL,
            [profile.user.email],
            fail_silently=False,
        )

@shared_task
def notify_superuser_new_registration(user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    send_mail(
        'New User Registration',
        f'A new user has registered: {user.username} (Email: {user.email})',
        settings.DEFAULT_FROM_EMAIL,
        [settings.SUPERUSER_EMAIL],
        fail_silently=False,
    )


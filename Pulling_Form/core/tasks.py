from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import UserProfile, Notification

def notify_superuser_new_registration(user):
    send_mail(
        'New User Registration',
        f'A new user has registered: {user.username} (Email: {user.email})',
        settings.DEFAULT_FROM_EMAIL,
        [settings.SUPERUSER_EMAIL],
        fail_silently=False,
    )

def notify_user_new_submission(user, submission):
    # Create dashboard notification
    Notification.objects.create(
        user=user,
        message=f'New form submission received (ID: {submission.id}) at {submission.created_at.strftime("%Y-%m-%d %H:%M")}',
        is_read=False
    )

def check_subscription_expiry():
    # Get all active subscriptions expiring in 5 days
    expiry_date = timezone.now().date() + timezone.timedelta(days=5)
    expiring_profiles = UserProfile.objects.filter(
        is_active=True,
        subscription_expiry_date=expiry_date
    )

    for profile in expiring_profiles:
        Notification.objects.create(
            user=profile.user,
            message=f'Your subscription will expire on {profile.subscription_expiry_date}. Please renew to continue using our services.',
            is_read=False
        )


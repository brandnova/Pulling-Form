import json
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinValueValidator, MaxValueValidator

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
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='form_submissions')
    data = models.JSONField(encoder=DjangoJSONEncoder)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} for {self.user_profile.user.username}"

    def get_display_fields(self):
        if isinstance(self.data, str):
            try:
                return json.loads(self.data).items()
            except json.JSONDecodeError:
                return []
        return self.data.items()

    def set_data(self, data_dict):
        if isinstance(data_dict, str):
            self.data = json.loads(data_dict)
        else:
            self.data = json.loads(json.dumps(data_dict, cls=DjangoJSONEncoder))



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

class CustomPage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_page')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Custom Page"

class CustomFormField(models.Model):
    FIELD_TYPES = (
        ('text', 'Text Input'),
        ('textarea', 'Text Area'),
        ('dropdown', 'Dropdown'),
        ('radio', 'Radio Buttons'),
        ('checkbox', 'Checkbox'),
        ('range', 'Range'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('time', 'Time'),
        ('password', 'Password'),
    )

    custom_page = models.ForeignKey(CustomPage, on_delete=models.CASCADE, related_name='form_fields')
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    options = models.TextField(blank=True, help_text="Comma-separated options for dropdown, radio, or checkbox")
    placeholder = models.CharField(max_length=255, blank=True)
    min_value = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    max_value = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(1000000)])
    min_length = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    max_length = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(1000)])
    description = models.TextField(blank=True, help_text="Optional description for this form field")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.get_field_type_display()})"




@receiver(post_save, sender=User)
def create_custom_page(sender, instance, created, **kwargs):
    if created:
        CustomPage.objects.create(user=instance, name=f"{instance.username}'s Page")

@receiver(post_save, sender=User)
def save_custom_page(sender, instance, **kwargs):
    instance.custom_page.save()
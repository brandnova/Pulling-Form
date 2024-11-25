from django.contrib import admin
from .models import UserProfile, FormSubmission, Subscription, SubscriptionSettings, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'unique_form_id', 'subscription_start_date', 'subscription_expiry_date', 'is_active')
    list_filter = ('is_active', 'subscription_start_date', 'subscription_expiry_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('unique_form_id',)

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'user_profile')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'user_profile__user__username')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'start_date', 'end_date', 'amount', 'paystack_reference', 'is_active')
    list_filter = ('start_date', 'end_date', 'is_active')
    search_fields = ('user_profile__user__username', 'paystack_reference')
    readonly_fields = ('start_date',)

@admin.register(SubscriptionSettings)
class SubscriptionSettingsAdmin(admin.ModelAdmin):
    list_display = ('price', 'duration_weeks')

    def has_add_permission(self, request):
        # Check if there's already a SubscriptionSettings object
        if SubscriptionSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Notification)
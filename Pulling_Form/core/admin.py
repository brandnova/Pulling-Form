import json
from django.contrib import admin
from .models import (
    SubscriptionSettings,
    UserProfile,
    FormSubmission,
    Subscription,
    Notification,
    CustomPage,
    CustomFormField,
)

# Inline for CustomFormField in CustomPage
class CustomFormFieldInline(admin.TabularInline):
    model = CustomFormField
    extra = 1
    fields = ('name', 'field_type', 'required', 'placeholder', 'order', 'options')
    readonly_fields = ('description',)
    ordering = ['order']


@admin.register(CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description')
    search_fields = ('user__username', 'name')
    inlines = [CustomFormFieldInline]


@admin.register(SubscriptionSettings)
class SubscriptionSettingsAdmin(admin.ModelAdmin):
    list_display = ('price', 'duration_weeks')
    list_editable = ('duration_weeks',)  
    list_display_links = ('price',)  
    search_fields = ('price',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'unique_form_id', 'is_active', 'subscription_start_date', 'subscription_expiry_date')
    search_fields = ('user__username', 'unique_form_id')
    list_filter = ('is_active', 'subscription_expiry_date')


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'created_at', 'data_summary')
    search_fields = ('user_profile__user__username', 'data')
    list_filter = ('created_at',)

    def data_summary(self, obj):
        return ', '.join([f"{k}: {v}" for k, v in json.loads(obj.data).items()][:3])  # Display only first 3 fields
    data_summary.short_description = "Data Summary"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'start_date', 'end_date', 'amount', 'is_active')
    search_fields = ('user_profile__user__username', 'paystack_reference')
    list_filter = ('is_active', 'start_date', 'end_date')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_summary', 'created_at', 'is_read')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read', 'created_at')

    def message_summary(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_summary.short_description = "Message"


@admin.register(CustomFormField)
class CustomFormFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'custom_page', 'required', 'order')
    search_fields = ('name', 'custom_page__user__username')
    list_filter = ('field_type', 'required')
    ordering = ('order',)

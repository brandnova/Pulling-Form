from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('form/<uuid:form_id>/', views.public_form, name='public_form'),
    path('form/success/', views.form_success, name='form_success'),
    path('subscription/initiate/', views.initiate_subscription, name='initiate_subscription'),
    path('subscription/verify/', views.verify_subscription, name='verify_subscription'),
    path('paystack/webhook/', views.paystack_webhook, name='paystack_webhook'),
    path('submission/edit/<int:submission_id>/', views.edit_form_submission, name='edit_form_submission'),
    path('submission/delete/<int:submission_id>/', views.delete_form_submission, name='delete_form_submission'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('notification/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('change_password/', views.change_password, name='change_password'),
]


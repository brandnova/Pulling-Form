from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.cache import cache
from django.db.models import Count
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm, PublicFormSubmissionForm, UserProfileUpdateForm
from .models import UserProfile, FormSubmission, Subscription, SubscriptionSettings, Notification
from .tasks import notify_superuser_new_registration, notify_user_new_submission
import uuid
import requests
from datetime import timedelta
import json

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            
            # Notify superuser about new registration
            notify_superuser_new_registration(user)
            
            return redirect('dashboard')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


def public_form(request, form_id):
    user_profile = get_object_or_404(UserProfile, unique_form_id=form_id)
    
    if not user_profile.has_active_subscription():
        return render(request, 'form_inactive.html')
    
    if request.method == 'POST':
        form = PublicFormSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user_profile = user_profile
            submission.save()
            
            # Create notification for new submission
            notify_user_new_submission(user_profile.user, submission)
            
            messages.success(request, "Form submitted successfully!")
            # Redirect to success page with the form URL
            form_url = reverse('public_form', kwargs={'form_id': user_profile.unique_form_id})
            return redirect(f"{reverse('form_success')}?form_url={form_url}")
    else:
        form = PublicFormSubmissionForm()
    
    return render(request, 'public_form.html', {'form': form})



def form_success(request):
    # Get the form URL from the query string
    form_url = request.GET.get('form_url')
    
    if not form_url:
        return HttpResponseBadRequest("Missing form URL")
    
    return render(request, 'form_success.html', {'form_url': form_url})



@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    form_url = request.build_absolute_uri(f'/form/{user_profile.unique_form_id}/')
    
    # Get form submissions
    submissions = user_profile.form_submissions.all().order_by('-created_at')
    
    # Setup pagination
    paginator = Paginator(submissions, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get form submission analytics
    total_submissions = submissions.count()
    submissions_by_date = user_profile.form_submissions.values('created_at__date').annotate(count=Count('id')).order_by('-created_at__date')[:7]
    
    # Get unread notifications
    unread_notifications = request.user.notifications.filter(is_read=False)
    
    context = {
        'form_url': form_url,
        'has_active_subscription': user_profile.has_active_subscription(),
        'page_obj': page_obj,
        'total_submissions': total_submissions,
        'submissions_by_date': submissions_by_date,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'dashboard.html', context)

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('dashboard')



@login_required
def initiate_subscription(request):
    subscription_settings = SubscriptionSettings.objects.first()
    if not subscription_settings:
        messages.error(request, "Subscription settings are not configured. Please contact the administrator.")
        return redirect('dashboard')

    amount = int(subscription_settings.price * 100)  # Convert to kobo
    user_profile = request.user.userprofile

    payload = {
        "amount": amount,
        "email": request.user.email,
        "callback_url": request.build_absolute_uri('/subscription/verify/'),
        "metadata": {
            "user_id": request.user.id,
            "user_profile_id": user_profile.id
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return redirect(data['data']['authorization_url'])
    else:
        messages.error(request, "Failed to initiate subscription. Please try again.")
        return redirect('dashboard')

@csrf_exempt
def verify_subscription(request):
    if request.method == 'GET':
        reference = request.GET.get('reference')
        
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        
        response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data['data']['status'] == 'success':
                user_id = data['data']['metadata']['user_id']
                user_profile = UserProfile.objects.get(user_id=user_id)
                
                subscription_settings = SubscriptionSettings.objects.first()
                subscription_end_date = timezone.now() + timedelta(weeks=subscription_settings.duration_weeks)
                
                # Create a new subscription
                Subscription.objects.create(
                    user_profile=user_profile,
                    end_date=subscription_end_date,
                    amount=data['data']['amount'] / 100,  # Convert from kobo to naira
                    paystack_reference=reference
                )
                
                # Update user profile
                user_profile.subscription_start_date = timezone.now()
                user_profile.subscription_expiry_date = subscription_end_date
                user_profile.is_active = True
                user_profile.save()
                
                messages.success(request, "Subscription successful!")
                
                # Send confirmation email
                send_mail(
                    'Subscription Confirmation',
                    f'Your subscription has been activated and will expire on {subscription_end_date.date()}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user_profile.user.email],
                    fail_silently=False,
                )
            else:
                messages.error(request, "Payment was not successful.")
        else:
            messages.error(request, "Failed to verify payment. Please contact support.")
        
        return redirect('dashboard')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def paystack_webhook(request):
    payload = json.loads(request.body)
    if payload['event'] == 'charge.success':
        reference = payload['data']['reference']
        subscription = Subscription.objects.filter(paystack_reference=reference).first()
        if subscription:
            subscription.is_active = True
            subscription.save()
    return JsonResponse({'status': 'success'})

@login_required
def edit_form_submission(request, submission_id):
    submission = get_object_or_404(FormSubmission, id=submission_id, user_profile=request.user.userprofile)
    if request.method == 'POST':
        form = PublicFormSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submission updated successfully.")
            return redirect('dashboard')
    else:
        form = PublicFormSubmissionForm(instance=submission)
    return render(request, 'edit_form_submission.html', {'form': form})

@login_required
def delete_form_submission(request, submission_id):
    submission = get_object_or_404(FormSubmission, id=submission_id, user_profile=request.user.userprofile)
    if request.method == 'POST':
        submission.delete()
        messages.success(request, "Form submission deleted successfully.")
        return redirect('dashboard')
    return render(request, 'delete_form_submission.html', {'submission': submission})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('dashboard')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        cache_key = f'password_reset_{email}'
        last_reset = cache.get(cache_key)

        if last_reset and (timezone.now() - last_reset).total_seconds() < 300:  # 5 minutes cooldown
            messages.error(self.request, "Please wait 5 minutes before requesting another password reset.")
            return self.form_invalid(form)

        cache.set(cache_key, timezone.now(), 300)  # Set cooldown
        return super().form_valid(form)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


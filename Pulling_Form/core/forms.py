import json
from datetime import date, datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from .models import CustomFormField, CustomPage, FormSubmission

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

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

class CustomPageForm(forms.ModelForm):
    class Meta:
        model = CustomPage
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'rows': 3}),
        }

class CustomFormFieldForm(forms.ModelForm):
    class Meta:
        model = CustomFormField
        fields = ['name', 'field_type', 'required', 'options', 'placeholder', 'min_value', 'max_value', 'min_length', 'max_length', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'field_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'required': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'options': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'rows': 3}),
            'placeholder': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'min_value': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'max_value': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'min_length': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'max_length': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'rows': 3}),
        }
        labels = {
            'name': 'Field Name',
            'field_type': 'Field Type',
            'required': 'Required',
            'options': 'Options (comma-separated)',
            'placeholder': 'Placeholder Text',
            'min_value': 'Minimum Value',
            'max_value': 'Maximum Value',
            'min_length': 'Minimum Length',
            'max_length': 'Maximum Length',
            'description': 'Field Description',
        }


class FormSubmissionEditForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = []

    def __init__(self, *args, **kwargs):
        custom_fields = kwargs.pop('custom_fields', None)
        super().__init__(*args, **kwargs)
        
        if custom_fields and self.instance:
            data = self.instance.data if isinstance(self.instance.data, dict) else {}
            
            for field in custom_fields:
                field_name = field.name
                field_value = data.get(field_name, '')
                
                field_kwargs = {
                    'label': field.name,
                    'required': field.required,
                    'help_text': field.description,
                    'initial': field_value
                }

                widget_attrs = {
                    'class': 'w-full px-3 py-2 border rounded-md',
                    'placeholder': field.placeholder or ''
                }

                if field.field_type == 'range':
                    min_val = field.min_value or 0
                    max_val = field.max_value or 100
                    widget_attrs.update({
                        'type': 'range',
                        'min': min_val,
                        'max': max_val,
                        'oninput': f'document.getElementById("range_value_{field_name}").value = this.value'
                    })
                    self.fields[field_name] = forms.IntegerField(
                        min_value=min_val,
                        max_value=max_val,
                        widget=forms.NumberInput(attrs=widget_attrs),
                        **field_kwargs
                    )
                elif field.field_type == 'radio':
                    choices = [(option.strip(), option.strip()) for option in field.options.split(',')]
                    self.fields[field_name] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect(attrs={'class': 'form-radio mr-2'}),
                        **field_kwargs
                    )
                elif field.field_type == 'checkbox':
                    choices = [(option.strip(), option.strip()) for option in field.options.split(',')]
                    # Convert string value to list if it's a string
                    if isinstance(field_value, str):
                        field_kwargs['initial'] = [field_value]
                    elif isinstance(field_value, list):
                        field_kwargs['initial'] = field_value
                    self.fields[field_name] = forms.MultipleChoiceField(
                        choices=choices,
                        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox mr-2'}),
                        **field_kwargs
                    )
                elif field.field_type == 'dropdown':
                    choices = [(option.strip(), option.strip()) for option in field.options.split(',')]
                    self.fields[field_name] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.Select(attrs=widget_attrs),
                        **field_kwargs
                    )
                elif field.field_type == 'textarea':
                    widget_attrs['rows'] = 3
                    self.fields[field_name] = forms.CharField(
                        widget=forms.Textarea(attrs=widget_attrs),
                        **field_kwargs
                    )
                else:
                    self.fields[field_name] = forms.CharField(
                        widget=forms.TextInput(attrs=widget_attrs),
                        **field_kwargs
                    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.data = self.cleaned_data
        if commit:
            instance.save()
        return instance


class DynamicFormSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        custom_fields = kwargs.pop('custom_fields', None)
        super().__init__(*args, **kwargs)

        if custom_fields:
            for field in custom_fields:
                field_kwargs = {
                    'label': field.name,
                    'required': field.required,
                    'help_text': field.description,
                }

                widget_attrs = {
                    'class': 'w-full px-3 py-2 border rounded-md',
                    'placeholder': field.placeholder or ''
                }

                if field.field_type == 'text':
                    self.fields[field.name] = forms.CharField(
                        widget=forms.TextInput(attrs=widget_attrs),
                        **field_kwargs
                    )
                elif field.field_type == 'textarea':
                    widget_attrs['rows'] = 3
                    self.fields[field.name] = forms.CharField(
                        widget=forms.Textarea(attrs=widget_attrs),
                        **field_kwargs
                    )
                elif field.field_type == 'dropdown':
                    choices = [(option.strip(), option.strip()) for option in field.options.split(',')]
                    self.fields[field.name] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.Select(attrs=widget_attrs),
                        **field_kwargs
                    )
                elif field.field_type == 'radio':
                    choices = [(option.strip(), option.strip()) for option in field.options.split(',')]
                    self.fields[field.name] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect(attrs={'class': 'mr-2'}),
                        **field_kwargs
                    )
                elif field.field_type == 'checkbox':
                    choices = [(option.strip(), option.strip()) for option in field.options.split(',')]
                    self.fields[field.name] = forms.MultipleChoiceField(
                        choices=choices,
                        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mr-2'}),
                        **field_kwargs
                    )
                elif field.field_type == 'range':
                    widget_attrs.update({
                        'type': 'range',
                        'min': field.min_value or 0,
                        'max': field.max_value or 100,
                        'oninput': f'this.nextElementSibling.value = this.value'
                    })
                    self.fields[field.name] = forms.IntegerField(
                        widget=forms.NumberInput(attrs=widget_attrs),
                        min_value=field.min_value or 0,
                        max_value=field.max_value or 100,
                        **field_kwargs
                    )
                elif field.field_type == 'email':
                    self.fields[field.name] = forms.EmailField(
                        widget=forms.EmailInput(attrs=widget_attrs),
                        **field_kwargs
                    )
                elif field.field_type == 'number':
                    self.fields[field.name] = forms.IntegerField(
                        widget=forms.NumberInput(attrs=widget_attrs),
                        min_value=field.min_value,
                        max_value=field.max_value,
                        **field_kwargs
                    )
                elif field.field_type == 'date':
                    self.fields[field.name] = forms.DateField(
                        widget=forms.DateInput(attrs={**widget_attrs, 'type': 'date'}),
                        **field_kwargs
                    )
                elif field.field_type == 'time':
                    widget_attrs['type'] = 'time'
                    self.fields[field.name] = forms.TimeField(
                        widget=forms.TimeInput(attrs=widget_attrs),
                        **field_kwargs
                    )
                elif field.field_type == 'password':
                    self.fields[field.name] = forms.CharField(
                        widget=forms.PasswordInput(attrs=widget_attrs),
                        **field_kwargs
                    )
import os

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import User

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

_INPUT = 'ts-input pl-9'
_INPUT_NO_ICON = 'ts-input'


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': True, 'class': _INPUT}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': _INPUT}),
    )


class GuardianRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': _INPUT_NO_ICON}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': _INPUT_NO_ICON}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': _INPUT}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': _INPUT}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': _INPUT}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return p2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password', 'class': _INPUT})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': _INPUT})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'guardian'
        if commit:
            user.save()
        return user


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget = forms.PasswordInput(attrs={
                'class': _INPUT,
                'placeholder': field.label,
            })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': _INPUT_NO_ICON}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': _INPUT_NO_ICON}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': _INPUT}),
        }

    def clean_avatar(self):
        f = self.cleaned_data.get('avatar')
        if f and hasattr(f, 'name'):
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                raise ValidationError(f'Only image files are allowed (JPG, PNG, GIF, WebP).')
            if f.size > 5 * 1024 * 1024:
                raise ValidationError('Avatar must be under 5 MB.')
        return f


# ── Task 5.7 — Admin User Management Forms ───────────────────────────

class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT_NO_ICON, 'placeholder': 'Set password'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': _INPUT_NO_ICON, 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': _INPUT_NO_ICON, 'placeholder': 'Last name'}),
            'username': forms.TextInput(attrs={'class': _INPUT_NO_ICON, 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': _INPUT_NO_ICON, 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': _INPUT_NO_ICON, 'placeholder': 'Phone'}),
            'role': forms.Select(attrs={'class': _INPUT_NO_ICON}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': _INPUT_NO_ICON}),
            'last_name': forms.TextInput(attrs={'class': _INPUT_NO_ICON}),
            'email': forms.EmailInput(attrs={'class': _INPUT_NO_ICON}),
            'phone': forms.TextInput(attrs={'class': _INPUT_NO_ICON}),
            'role': forms.Select(attrs={'class': _INPUT_NO_ICON}),
            'is_active': forms.CheckboxInput(),
        }

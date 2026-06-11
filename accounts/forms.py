from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User

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

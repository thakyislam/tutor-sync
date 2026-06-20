import re

from django import forms

from accounts.models import User
from core.models import Subject

from .models import Student

_INPUT = 'ts-input'
_TEXTAREA = 'ts-textarea'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'grade', 'subjects_needed', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': _INPUT, 'placeholder': 'Student full name',
            }),
            'grade': forms.TextInput(attrs={
                'class': _INPUT, 'placeholder': 'e.g. Grade 9, Year 11',
            }),
            'subjects_needed': forms.CheckboxSelectMultiple(),
            'notes': forms.Textarea(attrs={
                'class': _TEXTAREA, 'rows': 3,
                'placeholder': 'Any notes about learning needs...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects_needed'].queryset = Subject.objects.filter(is_active=True)
        self.fields['subjects_needed'].required = False
        self.fields['notes'].required = False


class GuardianCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': _INPUT, 'placeholder': 'Temporary password'}),
        label='Password',
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': _INPUT, 'placeholder': 'guardian@example.com'}),
            'phone': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '+1 555 000 0000'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        first = self.cleaned_data.get('first_name', '').lower()
        last = self.cleaned_data.get('last_name', '').lower()
        base = re.sub(r'[^a-z0-9]', '', f'{first}{last}') or self.cleaned_data['email'].split('@')[0]
        username, counter = base, 1
        while User.objects.filter(username=username).exists():
            username = f'{base}{counter}'
            counter += 1
        user.username = username
        user.set_password(self.cleaned_data['password'])
        user.role = 'guardian'
        if commit:
            user.save()
        return user

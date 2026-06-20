import os

from django import forms
from django.core.exceptions import ValidationError

from core.models import Subject

from .models import TutorApplication, TutorProfile

_INPUT = 'ts-input'
_TEXTAREA = 'ts-textarea'
_FILE = 'ts-file'

ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx'}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_document_file(f):
    ext = os.path.splitext(f.name)[1].lower()
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError(f'Only PDF, DOC, and DOCX files are allowed (got {ext}).')
    if f.size > MAX_UPLOAD_SIZE:
        raise ValidationError('File size must be under 10 MB.')


class TutorApplicationForm(forms.ModelForm):
    class Meta:
        model = TutorApplication
        fields = [
            'full_name', 'email', 'phone',
            'subjects', 'education', 'experience',
            'resume', 'id_document',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': _INPUT, 'placeholder': 'Your full legal name',
            }),
            'email': forms.EmailInput(attrs={
                'class': _INPUT, 'placeholder': 'you@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': _INPUT, 'placeholder': '+1 555 000 0000',
            }),
            'subjects': forms.CheckboxSelectMultiple(),
            'education': forms.Textarea(attrs={
                'class': _TEXTAREA, 'rows': 4,
                'placeholder': 'Describe your highest qualification and institution...',
            }),
            'experience': forms.Textarea(attrs={
                'class': _TEXTAREA, 'rows': 4,
                'placeholder': 'Describe your tutoring or teaching experience...',
            }),
            'resume': forms.FileInput(attrs={'class': _FILE}),
            'id_document': forms.FileInput(attrs={'class': _FILE}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.filter(is_active=True)
        self.fields['id_document'].required = False

    def clean_resume(self):
        f = self.cleaned_data.get('resume')
        if f:
            validate_document_file(f)
        return f

    def clean_id_document(self):
        f = self.cleaned_data.get('id_document')
        if f:
            validate_document_file(f)
        return f


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = TutorApplication
        fields = ['status', 'reviewer_notes']
        widgets = {
            'status': forms.Select(attrs={'class': _INPUT}),
            'reviewer_notes': forms.Textarea(attrs={
                'class': _TEXTAREA, 'rows': 5,
                'placeholder': 'Internal notes about this applicant...',
            }),
        }


class TutorProfileForm(forms.ModelForm):
    availability = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.Textarea(attrs={
            'class': _TEXTAREA, 'rows': 3,
            'placeholder': '{"mon": "9am-5pm", "fri": "9am-12pm"}',
        }),
    )

    class Meta:
        model = TutorProfile
        fields = [
            'bio', 'subjects', 'education_level', 'experience_yrs',
            'hourly_rate', 'availability', 'status', 'verified',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': _TEXTAREA, 'rows': 4,
                'placeholder': 'Brief professional bio...',
            }),
            'subjects': forms.CheckboxSelectMultiple(),
            'education_level': forms.TextInput(attrs={
                'class': _INPUT, 'placeholder': 'e.g. Bachelor\'s in Mathematics',
            }),
            'experience_yrs': forms.NumberInput(attrs={'class': _INPUT, 'min': 0}),
            'hourly_rate': forms.NumberInput(attrs={'class': _INPUT, 'min': 0, 'step': '0.01'}),
            'status': forms.Select(attrs={'class': _INPUT}),
            'verified': forms.CheckboxInput(),
        }

    def __init__(self, *args, is_admin=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.filter(is_active=True)
        self.fields['subjects'].required = False
        self.fields['bio'].required = False
        self.fields['education_level'].required = False
        self.fields['availability'].required = False
        if not is_admin:
            self.fields.pop('status')
            self.fields.pop('verified')

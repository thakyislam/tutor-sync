from django import forms

from tutors.models import TutorProfile

from .models import TutorRequest

_INPUT = 'ts-input'
_TEXTAREA = 'ts-textarea'


class TutorRequestForm(forms.ModelForm):
    class Meta:
        model = TutorRequest
        fields = ['student', 'subject', 'level', 'preferred_mode', 'budget', 'schedule_notes']
        widgets = {
            'student': forms.Select(attrs={'class': _INPUT}),
            'subject': forms.Select(attrs={'class': _INPUT}),
            'level': forms.TextInput(attrs={
                'class': _INPUT, 'placeholder': 'e.g. Beginner, GCSE, A-Level',
            }),
            'preferred_mode': forms.Select(attrs={'class': _INPUT}),
            'budget': forms.NumberInput(attrs={
                'class': _INPUT, 'placeholder': 'Hourly budget (optional)',
            }),
            'schedule_notes': forms.Textarea(attrs={
                'class': _TEXTAREA, 'rows': 4,
                'placeholder': 'Preferred days/times, any scheduling constraints...',
            }),
        }

    def __init__(self, *args, guardian_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        if guardian_profile is not None:
            self.fields['student'].queryset = guardian_profile.students.all()
        self.fields['student'].required = False
        self.fields['budget'].required = False
        self.fields['schedule_notes'].required = False


class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = TutorRequest
        fields = ['status', 'assigned_tutor', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': _INPUT}),
            'assigned_tutor': forms.Select(attrs={'class': _INPUT}),
            'admin_notes': forms.Textarea(attrs={
                'class': _TEXTAREA, 'rows': 4,
                'placeholder': 'Internal admin notes...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_tutor'].queryset = (
            TutorProfile.objects.filter(status='active').select_related('user')
        )
        self.fields['assigned_tutor'].required = False
        self.fields['admin_notes'].required = False

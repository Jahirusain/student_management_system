from django import forms
from .models import Result
from students.models import Student

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'marks']

        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'placeholder': 'Select student'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter subject name'
            }),
            'marks': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter marks'
            }),
        }

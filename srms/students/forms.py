from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter student full name'
            }),
            'roll_no': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter roll number'
            }),
        }

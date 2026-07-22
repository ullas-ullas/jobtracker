from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import JobApplication
from django.contrib.auth.models import User

from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .models import JobApplication


class JobApplicationForm(ModelForm):
    class Meta:
        model = JobApplication
        exclude = ['user']

        widgets = {
            'applied_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set today's date when creating a new job
        if not self.instance.pk:
            self.fields['applied_date'].initial = timezone.now().date()


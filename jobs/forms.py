from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import JobApplication
from django.contrib.auth.models import User
from django import forms

from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .models import JobApplication


class JobApplicationForm(ModelForm):
    class Meta:
        model = JobApplication
        exclude = ['user', 'follow_up_date', 'ai_analysis' , 'description']

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

        if self.instance.status == "Wishlist":
            self.fields.pop("applied_date")
            self.fields.pop("experience")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
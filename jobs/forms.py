from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import JobApplication
from django.contrib.auth.models import User

class JobApplicationForm(ModelForm):
    class Meta:
        model = JobApplication
        exclude = ['user']


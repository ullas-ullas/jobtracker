from django.db import models
from django.conf import settings
from datetime import date, datetime
from django.core.exceptions import ValidationError
# Create your models here.

class JobApplication(models.Model):
    status_options = {
        "Applied" : "Applied",
        "Accepted": "Accepted",
        "Rejected" : "Rejected"
    }
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length = 100)
    experience = models.IntegerField()
    location = models.CharField(max_length=100)
    status = models.CharField(choices=status_options, default="Applied")
    applied_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        today = date.today()
        if not self.pk:                 # wont run when updating existing application
            if JobApplication.objects.filter(company = self.company.strip(), job_title = self.job_title.strip()).exists():
                raise ValidationError("Duplicate job application on the same company and for the same role")
        if self.applied_date and self.applied_date > today:
            raise ValidationError("Applied Date shouldn't be in the future")  
        
    def save(self, *args , **kwargs):
        self.full_clean()
        super().save(*args , **kwargs)

    def __str__(self):
        return f"{self.company}_{self.user.username}"
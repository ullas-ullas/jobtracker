from django.db import models
from django.conf import settings
from datetime import date, datetime
from django.core.exceptions import ValidationError
from datetime import timedelta
# Create your models here.

class JobApplication(models.Model):
    status_options = {
        "Applied" : "Applied",
        "Accepted": "Accepted",
        "Rejected" : "Rejected"
    }
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length = 100)
    experience = models.IntegerField()
    location = models.CharField(max_length=100)
    status = models.CharField(choices=status_options, default="Applied")
    applied_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(blank=True, null=True)

    def clean(self):
        today = date.today()

        if self.company and self.job_title and self.user_id:
            qs = JobApplication.objects.filter(
                company__iexact=self.company.strip(),
                job_title__iexact=self.job_title.strip(),
                user=self.user,
            )

            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError(
                    "Duplicate job application on the same company and for the same role."
                )

        if self.applied_date and self.applied_date > today:
            raise ValidationError("Applied Date shouldn't be in the future")

    def save(self, *args, **kwargs):

        if self.applied_date:
            self.follow_up_date = self.applied_date + timedelta(days=7)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company}_{self.user.username}"
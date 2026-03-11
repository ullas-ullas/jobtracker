from django.db import models
from django.conf import settings
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

    def __str__(self):
        return f"{self.company}_{self.user.username}"
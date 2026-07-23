from celery import shared_task
from django.utils import timezone

from .models import JobApplication
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def check_followups():
    today = timezone.now().date()

    jobs = JobApplication.objects.filter(
        follow_up_date=today,
        status="Applied",
    )

    print(f"Found {jobs.count()} jobs to follow up.")

    for job in jobs:
        send_followup_email.delay(job.id)

@shared_task
def send_followup_email(job_id):

    job = JobApplication.objects.get(id=job_id)

    send_mail(
        subject=f"Follow up with {job.company}",
        message=(
            f"You applied for the role '{job.job_title}' at "
            f"{job.company}.\n\n"
            f"It's time to follow up with HR."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[job.user.email],
    )
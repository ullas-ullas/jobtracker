from django.contrib import admin
from .models import JobApplication

# Register your models here.


class AdminJobApplication(admin.ModelAdmin):
    def username_fn(self, obj):
        return obj.user.username
    list_display = ("user__username", "company", "status")
    list_filter = ("user__username","status")
    search_fields = ("location",)

admin.site.register(JobApplication, AdminJobApplication)

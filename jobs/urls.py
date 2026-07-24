from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.JobListView.as_view(), name="home"),
    path("job/<int:pk>/",views.JobDetailView.as_view(),name="job_detail"),
    path("create/", views.JobCreateView.as_view(), name="create_job"),
    path("update/<int:pk>/" , views.JobUpdateView.as_view(), name="update_job"),
    path("delete/<int:pk>/", views.JobDeleteView.as_view(), name="delete_job"),
    path("register/", views.UserCreationView.as_view(), name="register_user"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("export/", views.export_csv, name="export_csv"),
    path("search-jobs/", views.search_jobs_view,name="search_jobs"),
    path("track-job/", views.track_job, name="track_job"),
    path("job/<int:pk>/analyze/", views.analyze_job, name="analyze_job"),
]
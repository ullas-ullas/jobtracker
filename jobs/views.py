from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import JobApplication
from .forms import JobApplicationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages
import csv
from django.http import HttpResponse
from .forms import SignUpForm
from .services.api_service import search_jobs
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .services.ai_analysis import analyze_job_service
from collections import Counter



def home(request):
    return render(request, 'jobs.html')

class JobListView(LoginRequiredMixin, ListView):
    
    model = JobApplication
    # template_name = "templates/jobapplication_list.html"
    paginate_by = 6
    
    def get_queryset(self):
        query_ = self.request.GET.get("query")
        if query_:
            queryset_objs = JobApplication.objects.filter(Q(user = self.request.user) & (Q(job_title__icontains = query_) | Q(company__icontains = query_)))
            status = self.request.GET.get("fltr")
            if status:
                status = status.strip().title()
                queryset_objs = queryset_objs.filter(status = status)
            return queryset_objs

        queryset_objs = JobApplication.objects.filter(user = self.request.user)
        status = self.request.GET.get("fltr")
        if status:
            status = status.strip().title() 
            queryset_objs = queryset_objs.filter(status = status)

        return queryset_objs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_ = self.request.GET.get("query")
        if query_:
            search_value = query_
            context['search_val'] = search_value
            # print(search_value)
        
        status = self.request.GET.get('fltr')
        if status:
            context['status'] = status
        # print("-------------------")
        # print(context)
        # print("-------------------")
        return context

class JobDetailView(LoginRequiredMixin, DetailView):
    model = JobApplication
    template_name = "jobs/job_detail.html"

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    
class JobCreateView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    success_url = reverse_lazy('jobs:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Job Added Successfully")
        return super().form_valid(form)
    
class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = JobApplication
    form_class = JobApplicationForm
    success_url = reverse_lazy('jobs:home')

    def get_queryset(self):
        return JobApplication.objects.filter(user = self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Updated Successfully")
        return super().form_valid(form)
    
class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = JobApplication
    template_name = "jobs/confirm_delete.html"
    success_url = reverse_lazy('jobs:home')

    def get_queryset(self):
        return JobApplication.objects.filter(user = self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Jop application deleted Successfully")
        return super().form_valid(form)

class UserCreationView(CreateView):
    form_class = SignUpForm
    success_url= reverse_lazy('login')
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('jobs:home')
        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = "jobs/dashboard.html"

    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_datas = JobApplication.objects.aggregate(total = Count("id", filter = Q(user = self.request.user)),
                                                         accepted = Count("id", filter=Q(user = self.request.user, status = "Accepted")),
                                                         rejected = Count("id", filter=Q(user = self.request.user, status = "Rejected")),
                                                         applied = Count("id", filter=Q(user = self.request.user, status = "Applied")))
        context_data['total'] = context_datas['total']
        context_data['accepted'] = context_datas['accepted']
        context_data['rejected'] = context_datas['rejected']
        context_data['applied'] = context_datas['applied']

        return context_data


@login_required
def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_applications.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Company",
        "Job Title",
        "Location",
        "Experience",
        "Status",
        "Applied Date",
    ])

    jobs = JobApplication.objects.filter(user=request.user)

    for job in jobs:
        writer.writerow([
            job.company,
            job.job_title,
            job.location,
            job.experience,
            job.status,
            job.applied_date,
        ])

    return response

def search_jobs_view(request):

    keyword = request.GET.get("keyword", "").strip()

    jobs = None

    if keyword:
        jobs = search_jobs(keyword)

    return render(
        request,
        "jobs/search_jobs.html",
        {
            "jobs": jobs,
            "keyword": keyword,
        },
    )



@login_required
@require_POST
def track_job(request):

    company = request.POST["company"]
    title = request.POST["title"]
    description = request.POST.get("description", "")

    exists = JobApplication.objects.filter(
        user=request.user,
        company__iexact=company,
        job_title__iexact=title,
    ).exists()

    if exists:
        messages.warning(
            request,
            "You have already tracked this job."
        )

        return redirect(
            f"/search-jobs/?keyword={request.POST.get('keyword','')}"
        )

    JobApplication.objects.create(
        user=request.user,
        company=company,
        job_title=title,
        location=request.POST.get("location", ""),
        experience=None,
        status="Wishlist",
        job_url=request.POST.get("url", ""),
        description=description,
    )

    messages.success(
        request,
        "Job added to your dashboard!"
    )

    return redirect(
        f"/search-jobs/?keyword={request.POST.get('keyword','')}"
    )

@login_required
def analyze_job(request, pk):
    job = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user
    )

    if job.ai_analysis:
        return render(
            request,
            "jobs/job_analysis.html",
            {
                "job": job,
                "analysis": job.ai_analysis,
            },
        )

    try:
        analysis = analyze_job_service(
            title=job.job_title,
            company=job.company,
            description=job.description,
        )
        job.ai_analysis = analysis
        job.save(update_fields=["ai_analysis"])
    except Exception as e:
        messages.error(request, str(e))
        return redirect("jobs:job_detail", pk=job.pk)

    return render(
        request,
        "jobs/job_analysis.html",
        {
            "job": job,
            "analysis": analysis,
        },
    )
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import JobApplication
from .forms import JobApplicationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'jobs.html')

class JobListView(LoginRequiredMixin, ListView):
    
    model = JobApplication
    # template_name = "templates/jobapplication_list.html"
    paginate_by = 3
    
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
        print("-------------------")
        print(context)
        print("-------------------")
        return context
    
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
    form_class = UserCreationForm
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
                                                         applied = Count("id", filter=Q(user = self.request.user) & ~Q(status = "Accepted") & ~Q(status="Rejected")))
        context_data['total'] = context_datas['total']
        context_data['accepted'] = context_datas['accepted']
        context_data['rejected'] = context_datas['rejected']
        context_data['applied'] = context_datas['applied']

        return context_data
# tasks/views.py

from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Task, Category, PRIORITY_CHOICES
from .forms import TaskForm, CategoryForm


class LandingPageView(TemplateView):
    template_name = 'tasks/landing_page.html'
    
    def get(self, request, *args, **kwargs):
        # If the user is already logged in, send them to their dashboard instead
        if request.user.is_authenticated:
            return redirect('tasks:dashboard') # Redirect to the dedicated dashboard view
        # If not logged in, proceed to show the landing page as normal
        return super().get(request, *args, **kwargs)




    
class DashboardView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/dashboard.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        # Get only incomplete tasks for the logged-in user
        queryset = Task.objects.filter(user=self.request.user, is_completed=False)
        
        # Add priority filtering if requested
        priority = self.request.GET.get('priority')
        if priority and priority in [choice[0] for choice in PRIORITY_CHOICES]:
            queryset = queryset.filter(priority=priority)
        
        return queryset




class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    



class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('tasks:category_list')

    def form_valid(self, form):
        # Automatically set the user to the current logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)
    



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:dashboard')

    def get_form_kwargs(self):
        """Pass the current user to the form to filter categories"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Handle the "General" category logic
        if not Category.objects.filter(user=self.request.user).exists():
            # Create a General category if user has no categories
            Category.objects.create(user=self.request.user, name='General')
        
        # Automatically set the user to the current logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)
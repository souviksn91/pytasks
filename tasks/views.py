# tasks/views.py

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Task, Category, PRIORITY_CHOICES
from .forms import TaskForm, CategoryForm
from django.db.models import Q
from django.utils import timezone


# class LandingPageView(TemplateView):
#     template_name = 'tasks/landing_page.html'
    
#     def get(self, request, *args, **kwargs):
#         # If the user is already logged in, send them to their dashboard instead
#         if request.user.is_authenticated:
#             return redirect('tasks:dashboard') # Redirect to the dedicated dashboard view
#         # If not logged in, proceed to show the landing page as normal
#         return super().get(request, *args, **kwargs)






class AboutView(TemplateView):
    template_name = 'tasks/about.html'





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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total task count for the logged-in user
        context['total_tasks'] = Task.objects.filter(user=self.request.user).count()
        context['pending_tasks'] = Task.objects.filter(user=self.request.user, is_completed=False).count()
        context['completed_tasks'] = Task.objects.filter(user=self.request.user, is_completed=True).count()

        return context





    

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total category count
        context['total_categories'] = Category.objects.filter(user=self.request.user).count()
        return context
    






class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'tasks/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        # Ensure users can only view their own categories 
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get pending tasks for this specific category
        category = self.get_object()
        context['tasks'] = category.tasks.filter(is_completed=False)
        return context
    






class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('tasks:category_list')

    def get_form_kwargs(self):
        # Pass the current user to the form for validation 
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Set the user before saving
        form.instance.user = self.request.user
        return super().form_valid(form)
    








class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('tasks:category_list')

    def get_form_kwargs(self):
        # Pass the current user to the form for validation
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        # Ensure users can only edit their own categories 
        return Category.objects.filter(user=self.request.user)









class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('tasks:category_list')
    template_name = 'tasks/category_confirm_delete.html'  

    def get_queryset(self):
        # Ensure users can only delete their own categories 
        return Category.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Due to cascade delete, all associated tasks will be automatically deleted 
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)









class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        # Add current date to context for the date input min attribute 
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date().isoformat() 
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)









class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:dashboard')

    def get_form_kwargs(self):
        # Pass the current user to the form to filter categories
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        # Add current date to context for the date input min attribute 
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date().isoformat()  
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    








@login_required
def task_delete(request, pk):
    # Delete a task immediately without confirmation 
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('tasks:dashboard')
    








@login_required
def mark_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = True
    task.save()
    return redirect('tasks:dashboard')







class ArchivedTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/archives.html'
    context_object_name = 'completed_tasks'
    paginate_by = 10

    def get_queryset(self):
        # Show only completed tasks for the logged-in user 
        return Task.objects.filter(user=self.request.user, is_completed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add counts 
        context['total_completed'] = Task.objects.filter(
            user=self.request.user, 
            is_completed=True
        ).count()
        return context





@login_required
def delete_archived_task(request, pk):
    # Permanently delete a completed task from archives without confirmation 
    task = get_object_or_404(Task, pk=pk, user=request.user, is_completed=True)
    task.delete()
    return redirect('tasks:archives')


@login_required
def delete_all_archived_tasks(request):
    # Permanently delete all completed tasks without confirmation 
    if request.method == 'POST':
        # Only for the current user
        Task.objects.filter(user=request.user, is_completed=True).delete()
    return redirect('tasks:archives')










@login_required
def search_tasks(request):

    query = request.GET.get('q', '')
    tasks = Task.objects.none()  # Empty queryset by default
    
    if query:
        # Search title AND description of pending tasks for the current user
        tasks = Task.objects.filter(
            user=request.user,
            is_completed=False
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    return render(request, 'tasks/search.html', {
        'tasks': tasks,
        'query': query,
        'results_count': tasks.count()
    })


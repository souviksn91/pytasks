# tasks/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Choices for the priority field
PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('normal', 'Normal'),
    ('high', 'High'),
    ('critical', 'Critical'),
)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['user', 'name'] # A user can't have two categories with the same name

    def __str__(self):
        return f"{self.name} ({self.user.username})" 

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    is_completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        # Default ordering: show incomplete tasks first, then sort by priority and due date
        ordering = ['is_completed', '-priority', 'due_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # We can decide where to send the user after creating/editing a task.
        # Sending them to the dashboard is a safe bet.
        return reverse('tasks:dashboard')

    def is_overdue(self):
        """Helper method to check if the task is overdue."""
        return self.due_date < timezone.now().date() if not self.is_completed else False
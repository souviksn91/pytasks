# tasks/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

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
        return self.name 
    
    def get_absolute_url(self):
        return reverse('tasks:category_detail', kwargs={'pk': self.pk})

    # Get task counts
    def total_tasks(self):
        return self.tasks.count()

    def pending_tasks(self):
        return self.tasks.filter(is_completed=False).count()

    def completed_tasks(self):
        return self.tasks.filter(is_completed=True).count()






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
        # Sort by due date and priority
        ordering = ['is_completed', 'due_date', '-priority']

    def __str__(self):
        return self.title
    
    # def clean(self):
    #     super().clean()
    #     # Check if due_date is in the past (only for new tasks or when due_date is changed)
    #     if self.due_date and self.due_date < timezone.now().date():
    #         raise ValidationError({'due_date': 'Due date cannot be in the past.'})
        
    # def save(self, *args, **kwargs):
    #     self.full_clean()  # This runs the clean() method and all field validations
    #     super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        # Sending users to the dashboard
        return reverse('tasks:dashboard')

    def is_overdue(self):
        # Helper method to check if the task is overdue 
        return self.due_date < timezone.now().date() if not self.is_completed else False
    

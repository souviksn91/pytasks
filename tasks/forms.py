from django import forms
from .models import Task, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Work, Personal, Shopping'})
        }
        labels = {
            'name': 'Category Name'
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Task Title',
            'description': 'Description (Optional)',
            'due_date': 'Due Date',
            'priority': 'Priority',
            'category': 'Category'
        }

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # CRITICAL: Filter the category dropdown to only show categories for the current user.
        self.fields['category'].queryset = Category.objects.filter(user=user)
        # You can set a default choice for the category here if needed, but we'll handle "General" in the view.
from django import forms
from .models import Task, Category
from django.utils import timezone
from django.core.exceptions import ValidationError








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

    def __init__(self, *args, **kwargs):
        # Remove 'user' from kwargs before calling super()
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        """Check if category name already exists for this user"""
        name = self.cleaned_data.get('name')
        
        if self.user and name:
            # Check if a category with this name already exists for the user
            existing_category = Category.objects.filter(
                user=self.user, 
                name__iexact=name  # Case-insensitive check
            )
            
            # If we're editing an existing category, exclude it from the check
            if self.instance and self.instance.pk:
                existing_category = existing_category.exclude(pk=self.instance.pk)
            
            if existing_category.exists():
                raise forms.ValidationError("A category with this name already exists.")
        
        return name




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
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
        
        # Get or create the "General" category for this user
        general_category, created = Category.objects.get_or_create(
            user=user,
            name='General',
            defaults={'user': user}
        )
        
        # Now get ALL categories for this user, which now includes General
        user_categories = Category.objects.filter(user=user)
        
        # Set the queryset for the category field
        self.fields['category'].queryset = user_categories
        
        # Optional: Set "General" as the default selected choice
        self.fields['category'].initial = general_category
        
        # Set the minimum date for the date input field (HTML5 validation)
        self.fields['due_date'].widget.attrs['min'] = timezone.now().date().isoformat()

    def clean_due_date(self):
        """Custom validation to ensure due date is not in the past"""
        due_date = self.cleaned_data.get('due_date')
        
        if due_date and due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past. Please select today or a future date.")
        
        return due_date
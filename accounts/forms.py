# accounts/form.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        # label="Your First Name", 
        # widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}) \
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        # label="Your Last Name",
        # widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    username = forms.CharField(
        max_length=150,
        required=True  # Already a default True though
        # label="Choose a Username",
        # widget=forms.TextInput(attrs={'placeholder': 'Pick a unique username'})
    )
    email = forms.EmailField(
        required=True,
        # label="Your Email Address",
        # widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Remove all help text and validation for passwords
        self.fields['password1'].help_text = ''
        self.fields['password1'].validators = [] # Removes password validation
        
        self.fields['password2'].help_text = ''
        self.fields['password2'].validators = [] # Removes password validation
 
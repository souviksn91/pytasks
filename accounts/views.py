# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # log the user in automatically after signup
            return redirect('tasks:dashboard') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})



# We use Django's built-in LoginView and will configure it in urls.py
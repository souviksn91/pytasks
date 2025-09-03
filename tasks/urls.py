# tasks/urls.py

from django.urls import path
from . import views 

app_name = 'tasks'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task_create'),
    ]


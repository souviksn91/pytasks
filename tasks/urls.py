# tasks/urls.py

from django.urls import path
from . import views 

app_name = 'tasks'

urlpatterns = [
    # path('', views.LandingPageView.as_view(), name='landing_page'),
    path('', views.AboutView.as_view(), name='about'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/complete/', views.mark_task_done, name='task_complete'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('archives/', views.ArchivedTaskListView.as_view(), name='archives'),
    path('archives/<int:pk>/delete/', views.delete_archived_task, name='delete_archived_task'),
    path('archives/delete-all/', views.delete_all_archived_tasks, name='delete_all_archived'),
    path('search/', views.search_tasks, name='search'),

    ]


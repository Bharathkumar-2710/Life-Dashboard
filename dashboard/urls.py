from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🏠 Home / Dashboard
    path('', views.home, name='home'),

    # 📋 Task Management
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:id>/', views.edit_task, name='edit_task'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:id>/', views.toggle_complete, name='toggle_complete'),
    path('complete-all/', views.complete_all, name='complete_all'),

    # ⏱️ Time Tracking
    path('start/<int:id>/', views.start_task, name='start_task'),
    path('stop/<int:id>/', views.stop_task, name='stop_task'),

    # 🧲 Drag & Drop (AJAX)
    path('reorder/', views.reorder_tasks, name='reorder_tasks'),

    # 📊 Analytics / Features
    path('reminders/', views.reminders, name='reminders'),
    path('weekly/', views.weekly_progress, name='weekly'),
    path('streak/', views.streak, name='streak'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('profile/', views.profile, name='profile'),
    path('suggestions/', views.suggestions, name='suggestions'),

    # 📁 Import / Export
    path('import/', views.import_tasks, name='import_tasks'),
    path('export/', views.export_tasks, name='export_tasks'),

    # 🔐 Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
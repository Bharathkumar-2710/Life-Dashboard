from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),   # first page
    path('home/', views.home, name='home'),

    # 🔹 Task actions
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:id>/', views.toggle_complete, name='toggle_complete'),

    # 🔹 Auth
    path('register/', views.register, name='register'),

    # 🔹 New Features
    path('reminders/', views.reminders, name='reminders'),
    path('weekly/', views.weekly_progress, name='weekly'),
    path('streak/', views.streak, name='streak'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('complete-all/', views.complete_all, name='complete_all'),
    path('import/', views.import_tasks, name='import_tasks'),
    path('export/', views.export_tasks, name='export_tasks'),
    path('profile/', views.profile, name='profile'),
    path('suggestions/', views.suggestions, name='suggestions'),
]
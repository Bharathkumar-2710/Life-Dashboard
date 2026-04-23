from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),   # first page
    path('home/', views.home, name='home'),    # dashboard (after login)
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:id>/', views.toggle_complete, name='toggle_complete'),
    path('register/', views.register, name='register'),
]
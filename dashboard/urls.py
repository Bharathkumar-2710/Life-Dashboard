from django.urls import path
from .views import home, add_task

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_task, name='add_task'),
]
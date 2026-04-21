from django.urls import path
from .views import home, add_task, delete_task, toggle_complete

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_task, name='add_task'),
    path('delete/<int:id>/', delete_task, name='delete_task'),
    path('complete/<int:id>/', toggle_complete, name='complete_task'),
]
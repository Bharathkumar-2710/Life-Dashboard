from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('add/', views.add_task, name='add_task'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:id>/', views.toggle_complete, name='toggle_complete'),

    # 🔥 New
    path('start/<int:id>/', views.start_task, name='start_task'),
    path('stop/<int:id>/', views.stop_task, name='stop_task'),
    path('reorder/', views.reorder_tasks, name='reorder_tasks'),

    path('export/', views.export_tasks, name='export_tasks'),
    path('register/', views.register, name='register'),
]
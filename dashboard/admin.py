from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'completed', 'due_date')
    list_filter = ('completed', 'category')
    search_fields = ('title',)
    ordering = ('-created_at',)


admin.site.register(Task, TaskAdmin)
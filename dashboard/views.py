import json
from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()

    # Category stats
    categories = {}
    for task in tasks:
        categories[task.category] = categories.get(task.category, 0) + 1

    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'category_data': json.dumps(categories, cls=DjangoJSONEncoder)
    }

    return render(request, 'home.html', context)
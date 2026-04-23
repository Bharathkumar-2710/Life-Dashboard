from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder


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

    return render(request, 'home.html', {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'category_data': json.dumps(categories, cls=DjangoJSONEncoder)
    })


@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        due_date = request.POST.get('due_date')

        if title:
            Task.objects.create(
                title=title,
                category=category,
                due_date=due_date,
                user=request.user
            )
    return redirect('home')   # ✅ better than '/'


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)  # ✅ SECURITY FIX
    task.delete()
    return redirect('home')


@login_required
def toggle_complete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)  # ✅ SECURITY FIX
    task.completed = not task.completed
    task.save()
    return redirect('home')
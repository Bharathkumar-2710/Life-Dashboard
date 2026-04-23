from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')  # 👈 show login/register page

    tasks = Task.objects.filter(user=request.user)

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()

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
    return redirect('home')


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('home')


@login_required
def toggle_complete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('home')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created! Login now.")
        return redirect("login")

    return render(request, "registration/register.html")
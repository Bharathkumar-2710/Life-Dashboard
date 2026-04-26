from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from datetime import date, timedelta
from django.utils import timezone
import json, csv
from collections import defaultdict


# ---------------- HOME ----------------
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')

    tasks = Task.objects.filter(user=request.user)

    # 🔍 Filters
    if request.GET.get('q'):
        tasks = tasks.filter(title__icontains=request.GET['q'])

    if request.GET.get('category'):
        tasks = tasks.filter(category=request.GET['category'])

    if request.GET.get('priority'):
        tasks = tasks.filter(priority=request.GET['priority'])

    # 📊 Stats
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()
    completion_rate = (completed / total * 100) if total else 0

    # 📅 Date logic
    today = date.today()
    overdue = tasks.filter(due_date__lt=today, completed=False)
    today_tasks = tasks.filter(due_date=today, completed=False)

    # 📊 Category data
    categories = {}
    for task in tasks:
        categories[task.category] = categories.get(task.category, 0) + 1

    # 📈 REAL weekly data
    week_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    weekly_data = defaultdict(int)

    for task in tasks.filter(completed=True, completed_at__isnull=False):
        d = task.completed_at.date()
        if d in week_days:
            weekly_data[d.strftime("%a")] += 1

    weekly_labels = [d.strftime("%a") for d in week_days]
    weekly_values = [weekly_data[label] for label in weekly_labels]

    return render(request, 'home.html', {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': completion_rate,
        'overdue': overdue,
        'today_tasks': today_tasks,
        'category_data': json.dumps(categories),
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_values': json.dumps(weekly_values),
    })


# ---------------- TASK ----------------
@login_required
def add_task(request):
    if request.method == "POST":
        Task.objects.create(
            title=request.POST.get('title'),
            category=request.POST.get('category'),
            priority=request.POST.get('priority'),
            due_date=request.POST.get('due_date'),
            user=request.user
        )
    return redirect('home')


@login_required
def delete_task(request, id):
    get_object_or_404(Task, id=id, user=request.user).delete()
    return redirect('home')


@login_required
def toggle_complete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('home')


# ---------------- TIME TRACKING ----------------
@login_required
def start_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.start_time = timezone.now()
    task.save()
    return redirect('home')


@login_required
def stop_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if task.start_time:
        duration = (timezone.now() - task.start_time).seconds
        task.total_time += duration
        task.start_time = None
        task.save()

    return redirect('home')


# ---------------- DRAG SAVE ----------------
@login_required
def reorder_tasks(request):
    if request.method == "POST":
        order = json.loads(request.body)

        for index, task_id in enumerate(order):
            Task.objects.filter(id=task_id, user=request.user).update(order=index)

        return JsonResponse({"status": "ok"})


# ---------------- EXPORT ----------------
@login_required
def export_tasks(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Priority', 'Due Date', 'Completed'])

    for task in Task.objects.filter(user=request.user):
        writer.writerow([task.title, task.category, task.priority, task.due_date, task.completed])

    return response


# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username exists")
            return redirect("register")

        User.objects.create_user(username=username, password=password)
        return redirect("login")

    return render(request, "registration/register.html")
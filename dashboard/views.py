from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from datetime import date, timedelta
import json
import csv
from django.core.serializers.json import DjangoJSONEncoder


# ---------------- HOME ----------------
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')

    tasks = Task.objects.filter(user=request.user)

    # 🔍 Search
    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(title__icontains=query)

    # 🏷️ Category Filter
    category_filter = request.GET.get('category')
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    # 🎯 Priority Filter
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    # 🔄 Sorting
    sort = request.GET.get('sort')
    if sort == "due":
        tasks = tasks.order_by('due_date')
    elif sort == "priority":
        tasks = tasks.order_by('priority')

    # 📊 Stats
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()
    completion_rate = (completed / total * 100) if total > 0 else 0

    # 📅 Date logic
    today = date.today()
    overdue_tasks = tasks.filter(due_date__lt=today, completed=False)
    today_tasks = tasks.filter(due_date=today, completed=False)

    # 📊 Category Chart
    categories = {}
    category_stats = {}

    for task in tasks:
        cat = task.category

        categories[cat] = categories.get(cat, 0) + 1

        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "completed": 0}

        category_stats[cat]["total"] += 1
        if task.completed:
            category_stats[cat]["completed"] += 1

    return render(request, 'home.html', {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': completion_rate,
        'overdue': overdue_tasks,
        'today_tasks': today_tasks,
        'category_data': json.dumps(categories, cls=DjangoJSONEncoder),
        'category_stats': json.dumps(category_stats)
    })


# ---------------- ADD TASK ----------------
@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        if title:
            Task.objects.create(
                title=title,
                category=category,
                due_date=due_date,
                priority=priority,
                user=request.user
            )
            messages.success(request, "Task added successfully")

    return redirect('home')


# ---------------- EDIT TASK ----------------
@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == "POST":
        task.title = request.POST.get('title')
        task.category = request.POST.get('category')
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority')
        task.save()

        messages.success(request, "Task updated successfully")
        return redirect('home')

    return render(request, 'edit_task.html', {'task': task})


# ---------------- DELETE TASK ----------------
@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    messages.warning(request, "Task deleted")
    return redirect('home')


# ---------------- TOGGLE COMPLETE ----------------
@login_required
def toggle_complete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()

    if task.completed:
        messages.success(request, "Task marked as completed")
    else:
        messages.info(request, "Task marked as pending")

    return redirect('home')


# ---------------- REMINDERS ----------------
@login_required
def reminders(request):
    today = date.today()

    due_today = Task.objects.filter(user=request.user, due_date=today, completed=False)
    overdue = Task.objects.filter(user=request.user, due_date__lt=today, completed=False)

    return render(request, "reminders.html", {
        "due_today": due_today,
        "overdue": overdue
    })


# ---------------- WEEKLY PROGRESS ----------------
@login_required
def weekly_progress(request):
    today = date.today()
    week_start = today - timedelta(days=7)

    tasks = Task.objects.filter(user=request.user, due_date__gte=week_start)

    total = tasks.count()
    completed = tasks.filter(completed=True).count()

    return render(request, "weekly.html", {
        "total": total,
        "completed": completed
    })


# ---------------- STREAK ----------------
@login_required
def streak(request):
    tasks = Task.objects.filter(user=request.user, completed=True).order_by('-due_date')

    streak_count = 0
    current_day = date.today()

    for task in tasks:
        if task.due_date == current_day:
            streak_count += 1
            current_day -= timedelta(days=1)
        else:
            break

    return render(request, "streak.html", {"streak": streak_count})


# ---------------- CALENDAR ----------------
@login_required
def calendar_view(request):
    tasks = Task.objects.filter(user=request.user)

    events = []
    for task in tasks:
        if task.due_date:
            events.append({
                "title": task.title,
                "date": task.due_date.strftime("%Y-%m-%d"),
                "completed": task.completed
            })

    return render(request, "calendar.html", {
        "events": json.dumps(events)
    })


# ---------------- COMPLETE ALL ----------------
@login_required
def complete_all(request):
    Task.objects.filter(user=request.user, completed=False).update(completed=True)
    messages.success(request, "All tasks completed!")
    return redirect('home')


# ---------------- EXPORT CSV ----------------
@login_required
def export_tasks(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Priority', 'Due Date', 'Completed'])

    tasks = Task.objects.filter(user=request.user)

    for task in tasks:
        writer.writerow([
            task.title,
            task.category,
            task.priority,
            task.due_date,
            task.completed
        ])

    return response


# ---------------- IMPORT CSV ----------------
@login_required
def import_tasks(request):
    if request.method == "POST":
        file = request.FILES["file"]
        decoded = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded)

        next(reader)

        for row in reader:
            Task.objects.create(
                title=row[0],
                category=row[1],
                priority=row[2],
                due_date=row[3],
                completed=row[4] == "True",
                user=request.user
            )

        messages.success(request, "Tasks imported!")
        return redirect('home')

    return render(request, "import.html")


# ---------------- PROFILE ----------------
@login_required
def profile(request):
    tasks = Task.objects.filter(user=request.user)

    return render(request, "profile.html", {
        "total": tasks.count(),
        "completed": tasks.filter(completed=True).count(),
        "pending": tasks.filter(completed=False).count()
    })


# ---------------- SUGGESTION ----------------
@login_required
def suggestions(request):
    task = Task.objects.filter(user=request.user, completed=False).order_by('due_date').first()

    return render(request, "suggestion.html", {
        "task": task
    })


# ---------------- REGISTER ----------------
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
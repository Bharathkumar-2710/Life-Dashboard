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

    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'category_data': json.dumps(categories, cls=DjangoJSONEncoder)
    }

    return render(request, 'home.html', context)
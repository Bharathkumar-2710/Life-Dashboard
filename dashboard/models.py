from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ link to user
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="General")  # ✅ added
    due_date = models.DateField(null=True, blank=True)  # ✅ optional
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ extra useful

    def __str__(self):
        return self.title
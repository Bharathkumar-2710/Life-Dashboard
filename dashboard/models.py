from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="General")

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    # 🔥 NEW FEATURES
    start_time = models.DateTimeField(null=True, blank=True)
    total_time = models.IntegerField(default=0)  # seconds
    order = models.IntegerField(default=0)  # drag & drop order

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.priority})"
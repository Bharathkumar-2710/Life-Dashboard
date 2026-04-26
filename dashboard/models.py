from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    # 🔗 User relation
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 📝 Basic Info
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="General")

    # 🎯 Priority Choices
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    # 📅 Dates
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Status
    completed = models.BooleanField(default=False)

    # ⚡ Optional: auto-update when completed
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        from django.utils import timezone

        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None

        super().save(*args, **kwargs)

    # 🔽 Default ordering (important)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.priority})"
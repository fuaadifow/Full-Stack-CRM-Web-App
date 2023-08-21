from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = (
    ('high', 'High priority'),
    ('medium', 'Medium priority'),
    ('low', 'Low priority'),
)

STATUS_CHOICES = (
    ('not_started', 'Not started'),
    ('in_progress', 'In progress'),
    ('completed', 'Completed'),
)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_to_name = models.CharField(max_length=100, blank=True, null=True)
    assigned_to_position = models.CharField(max_length=100, blank=True, null=True)
    assigned_to_email = models.EmailField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return self.title


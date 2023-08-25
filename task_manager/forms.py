from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to_name', 'assigned_to_position', 'assigned_to_email',
                  'due_date', 'status']
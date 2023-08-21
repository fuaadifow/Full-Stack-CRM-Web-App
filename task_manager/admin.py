from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'assigned_to_name', 'due_date', 'status')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'description', 'assigned_to_name')
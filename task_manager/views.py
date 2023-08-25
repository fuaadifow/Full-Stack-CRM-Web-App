from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import F, Case, When, Value, IntegerField
from datetime import datetime, timedelta

# the code below is a sorting algorithm which fetches tasks from the database for the currently logged-in user, calculates the urgency of each task based on its due date, and sorts the tasks based on urgency, due date, and priority
def task_list(request):
    user = request.user
    today = datetime.now()
    one_week_later = today + timedelta(days=7)
    tasks = Task.objects.filter(
        user=user
    ).annotate(
        urgency=Case(
            When(due_date__lte=one_week_later, then=Value(1)),
            default=Value(2),
            output_field=IntegerField()
        )
    ).order_by('urgency', F('due_date').asc(nulls_last=True), 'priority')

    return render(request, 'task_manager/task_list.html', {'tasks': tasks})


def create_or_edit_task(request, task_id=None):
    if task_id:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = None
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)  
            task.user = request.user 
            task.save()
            return redirect('task_list')

    else:
        if task and  task.due_date:
            initial_data = {'due_date': task.due_date.strftime('%Y-%m-%dT%H:%M') if task else None}
            form = TaskForm(instance=task, initial=initial_data)
        else:

            form = TaskForm(instance=task)

    return render(request, 'task_manager/task_form.html', {'form': form})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

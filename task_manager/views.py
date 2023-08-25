from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.db.models import F, Case, When, Value


def task_list(request):
    user = request.user

    tasks = Task.objects.filter(
        user=user
    ).order_by(
        Case(
            When(due_date__isnull=True, then=Value(timezone.datetime.max)),
            default=F('due_date'),
        )
    )

    for task in tasks:
        due_date = task.due_date
        if due_date:
            time_diff = (due_date - timezone.now()).days
            if time_diff < 7:
                task.priority = 'High Priority'
            elif 7 <= time_diff < 14:
                task.priority = 'Medium Priority'
            else:
                task.priority = 'Low Priority'
        else:
            task.priority = 'No Due Date'

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

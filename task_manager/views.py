from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
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
        form = TaskForm(instance=task)

    return render(request, 'task_manager/task_form.html', {'form': form})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    print('test')
    return redirect('task_list')

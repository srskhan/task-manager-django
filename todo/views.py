from django.shortcuts import render,redirect,get_object_or_404
from .models import Todo
# Create your views here.

def todo_list(request):
    
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'completed':
        todos = Todo.objects.filter(is_completed=True)
    elif filter_type == 'pending':
        todos = Todo.objects.filter(is_completed=False)
    else:
        todos = Todo.objects.all()

    if request.method == 'POST':

        # ADD
        if "add_task" in request.POST:
            title = request.POST.get('title')

            if title:
                Todo.objects.create(
                    title=title
                )
            return redirect('todo_list')

        # EDIT
        if 'edit_task' in request.POST:
            task_id = request.POST.get('task_id')
            new_title = request.POST.get('new_title')

            todo = get_object_or_404(Todo, id=task_id)
            todo.title = new_title
            todo.save()
            return redirect('todo_list')

        # DELETE
        if 'delete_task' in request.POST:
            task_id = request.POST.get('task_id')
            todo = get_object_or_404(Todo, id=task_id)
            todo.delete()
            return redirect('todo_list')

        # CLEAR
        if 'clear_all' in request.POST:
            Todo.objects.all().delete()
            return redirect('todo_list')

        # MARK DONE
        if 'toggle_complete' in request.POST:
            task_id = request.POST.get('task_id')
            todo = get_object_or_404(Todo, id=task_id)
            todo.is_completed = not todo.is_completed
            todo.save()
            return redirect('todo_list')

    return render(request, 'todo/list.html', {
        'todos': todos,
        'task_count': todos.count(),
        'current_filter': filter_type
    })
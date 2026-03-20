from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoTask
from .forms import TodoTaskForm

# Todoリスト一覧、作成
def todo_list(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id: #更新処理時
            task = get_object_or_404(TodoTask, id=task_id)
            form = TodoTaskForm(request.POST, instance=task)
        else: #新規作成時
            form = TodoTaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('todo_list')
        else:
            print(form.errors)
    else:
        form = TodoTaskForm()

    tasks = TodoTask.objects.all()
    
    return render(request, 'todo/todo_list.html', {
        'tasks': tasks,
        'form': form,
    })

# def todo_create(request):
#     if request.method == 'POST':
#         form = TodoTaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('todo_list')
#     else:
#         form = TodoTaskForm()
#     return render(request, 'todo/todo_list.html', {'form': form})
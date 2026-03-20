from django.shortcuts import render, redirect, get_list_or_404
from .models import TodoTask
#from .forms import TodoTaskForm

# Todoリスト一覧
def todo_list(request):
    tasks = TodoTask.objects.all()
    return render(request, 'todo/todo_list.html', {'tasks': tasks})


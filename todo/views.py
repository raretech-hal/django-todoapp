from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoTask, Category
from .forms import TodoTaskForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.db.models import Count

# Todoリスト一覧、作成、編集
@login_required
def todo_list(request):
    tasks = TodoTask.objects.filter(user=request.user)

    now = datetime.datetime.now()
    #scheduled = tasks.filter(duedate__isnull=False, duedate__gte=now)
    base_tasks = tasks 
    scheduled = base_tasks.filter(duedate__isnull=False)
    overdue = base_tasks.filter(duedate__isnull=False, duedate__lt=now)
    
    status = request.GET.get('status')
    category_id = request.GET.get('category_id')
    # ステータスで絞る
    if status == 'scheduled':
        tasks = tasks.filter(duedate__isnull=False)
    elif status == 'overdue':
        tasks = tasks.filter(duedate__lt=now)
    # カテゴリで絞る
    if category_id:
        tasks = tasks.filter(category=category_id)
    
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id: #更新処理時
            task = get_object_or_404(TodoTask, id=task_id, user=request.user)
            form = TodoTaskForm(request.POST, instance=task)
        else: #新規作成時
            form = TodoTaskForm(request.POST)

        if form.is_valid():
            todo = form.save(commit=False) #commit=falseとして、この時点ではまだ保存しない
            if not task_id:
                todo.user = request.user
            todo.save()
            return redirect('todo_list')
        else:
            print(form.errors)
    else:
        form = TodoTaskForm()

    categories = Category.objects.filter(user=request.user).annotate(
        task_count=Count('tasks')
    )
    
    return render(request, 'todo/todo_list.html', {
        'tasks': tasks,
        'base_tasks': base_tasks,
        'categories': categories,
        'scheduled': scheduled,
        'overdue': overdue,
        'form': form,
    })

# Todoリスト削除
def todo_delete(request, task_id):
    print("oko")
    print(task_id)
    if request.method == 'POST':
        task = get_object_or_404(TodoTask, id=task_id, user=request.user)
        task.delete()
    
    return redirect('todo_list')

# Todoのcompletedの更新
def toggle_completed(request, task_id):
    task= get_object_or_404(TodoTask, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('todo_list')



## カテゴリー
@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if name:
            category, created = Category.objects.get_or_create(
                user=request.user,
                name=name
            )
            if created:
                messages.success(request, f'カテゴリ「{name}」を追加しました。')
            else:
                messages.info(request, f'カテゴリ「{name}」はすでに存在します。')
        else:
            messages.error(request, 'カテゴリ名を入力してください。')

    return redirect('todo_list')


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        category.delete()
        messages.success(request, f'カテゴリ「{category.name}」を削除しました。')

    return redirect('todo_list')


## 認証
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールを更新しました。')
        else:
            print(form.errors)
            messages.error(request, f'プロフィールを更新できませんでした: {form.errors}')

    return redirect('todo_list')


# def todo_create(request):
#     if request.method == 'POST':
#         form = TodoTaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('todo_list')
#     else:
#         form = TodoTaskForm()
#     return render(request, 'todo/todo_list.html', {'form': form})
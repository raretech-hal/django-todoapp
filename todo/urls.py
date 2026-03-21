from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('delete/<int:task_id>/', views.todo_delete, name='todo_delete'),
    path('toggle/<int:task_id>/', views.toggle_completed, name='toggle_completed')
]

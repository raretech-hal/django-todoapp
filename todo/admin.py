from django.contrib import admin
from .models import TodoTask, Category, Profile

# Register your models here.
admin.site.register(TodoTask)
admin.site.register(Category)
admin.site.register(Profile)
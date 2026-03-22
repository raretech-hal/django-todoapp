from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ModelBaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Category(ModelBaseClass):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TodoTask(ModelBaseClass):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todo_tasks",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    duedate = models.DateField(blank=True, null=True) 
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    # category = models.ManyToManyField(
    #     Category,
    #     blank=True,
    #     related_name="tasks",
    # )

    def __str__(self) -> str:
        return self.title
    
class Profile(ModelBaseClass):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField("表示名", max_length=100, blank=True)

    def __str__(self):
        return self.display_name or self.user.username
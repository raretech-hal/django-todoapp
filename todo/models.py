from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TodoTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    duedate = models.DateField(blank=True, null=True) 
    category = models.ManyToManyField(
        Category,
        blank=True,
        related_name="tasks",
    )

    def __str__(self) -> str:
        return self.title
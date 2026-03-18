from django.db import models

# Create your models here.
class TodoTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
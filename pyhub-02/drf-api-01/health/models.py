from django.db import models


# Todo.objects.create(message="...")


class Todo(models.Model):
    message = models.CharField(max_length=1000)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

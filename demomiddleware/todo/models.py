from django.db import models

# Create your models here.
class ToDo(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=100)
    is_done=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.title


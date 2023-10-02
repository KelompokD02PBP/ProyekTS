from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    subject = models.TextField()
    
    def __str__(self) -> str:
        return str(self.title)+" "+str(self.author)
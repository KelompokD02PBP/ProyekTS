from django.db import models
from katalog.models import Book
from django.contrib.auth.models import User

# Create your models here.


class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user.id)+"likes"+str(self.book.title)

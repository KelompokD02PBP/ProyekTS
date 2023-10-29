from django.db import models
from katalog.models import Book
from django.contrib.auth.models import User
from django.utils import timezone 

# Create your models here.


class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user.id)+"likes"+str(self.book.title)

# MODEL User yang ada info lain selain user name dan password
class ProfileUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    email = models.EmailField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    address = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.user} {self.email} "
    
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.user} commented {self.comment}"
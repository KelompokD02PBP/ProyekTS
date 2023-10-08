from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    isbn = models.TextField()
    title = models.TextField()
    author = models.TextField()
    # subject = models.TextField()
    year_of_publish = models.IntegerField()
    publisher = models.TextField()
    image_url_s = models.TextField()
    image_url_m = models.TextField()
    image_url_l = models.TextField()
    
    def __str__(self) -> str:
        return "ISBN: "+str(self.isbn)+ " ; Title: "+str(self.title)+" ; Author: "+str(self.author)
    

class AppUser(models.Model):
    user = models.OneToOneField(on_delete= models.CASCADE, to=User)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    liked_books = models.ManyToManyField(Book)

    def __str__(self):
        return self.user.get_username() +" liked books: "+str(self.liked_books.all())
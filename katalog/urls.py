from django.urls import path
from .views import *
urlpatterns = [
    path('get-books', get_books, name="get-books" ),
]

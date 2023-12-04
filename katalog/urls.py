from django.urls import path
from .views import *
urlpatterns = [
    path('get-books', get_books, name="get-books" ),
    path('get-books-json', get_books_json, name="get-books-json" ),
    path('search-books-json/<str:book_name>', get_search_book_json, name="search-books-json" ),
    path('search-books-json/', get_books_json, name="get-books" ),
    path('sort-books-json/', get_sorted_book_json, name="sorted-books" ),
    path('sort-books-json/<str:book_name>', get_sorted_book_json, name="sorted-books" ),
]

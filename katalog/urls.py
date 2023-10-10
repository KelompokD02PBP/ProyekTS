from django.urls import path
from .views import *
urlpatterns = [
    path('make-katalog', make_book_dataframe, name="make-book"), # USER GAK BOLEH AKSES
    path('get-books', get_books, name="get-books" ),
    # path('search/<str:searched_book>', search_book, name="search-books" ),
]

from django.shortcuts import render
import pandas as pd
from .models import Book
from django.http import HttpResponse
from proyekts.settings import BASE_DIR
import os
# Create your views here.
def make_book_dataframe(request):
    source= os.path.join(BASE_DIR, 'datasets')
    res=""
    book_dataset = pd.read_csv(source+'\\pg_catalog.csv', index_col="Text#", dtype=object)
    for i in range(100):
        book = Book(
            title=book_dataset.iloc[[i]]['Title'],
            author = book_dataset.iloc[[i]]['Authors'],
            subject = book_dataset.iloc[[1]]['Subjects']
        )
        book.save()
        print(book)
        res+=str(book)+"\n"

    return HttpResponse( res)
    
def get_books(request):
    books = Book.objects.all()
    for b in books:
        print(b)
from django.shortcuts import render
import pandas as pd
from .models import Book
from django.http import HttpResponse
from proyekts.settings import BASE_DIR
import os
# Create your views here.

# USER GAK BOLEH AKSES
def make_book_dataframe(request):
    source= os.path.join(BASE_DIR, 'datasets')
    res=""
    book_dataset = pd.read_csv(source+'\\pg_catalog.csv', index_col="Text#", dtype=object)
    for i in range(100):
        name = book_dataset.iloc[[i]]['Title']
        name = str(name)
        name.replace("\n", " ")
        name.replace("\r", " ")
        book = Book(
            title=name[5:],
            author = book_dataset.iloc[[i]]['Authors'],
            subject = book_dataset.iloc[[1]]['Subjects']
        )
        book.save()
        print(book)
        res+=str(book)+"\n"

    return HttpResponse(res)
    
def search_book(request, searched_book):
    all_books = Book.objects.all()
    all_books_name = [b.title for b in all_books]
    res=set()
    name_split = searched_book.split(" ")

    # for i in range(len(all_books_name)):
    #     lowered_name = searched_book.lower()
    #     lowered_title = all_books_name[i].lower()
    #     if lowered_name in  lowered_title:
    #         res.add(all_books_name[i])
    add=False
    for kata in name_split:
        for buku in all_books_name:
            buku_split = buku.split()
            if(kata in buku_split):
                res.add(buku)
                add=True
                break
            if(not add):
                for kata_buku in buku_split:
                    if(kata_buku in name_split):
                        res.add(buku)

    # for i in range(len(all_books_name)):
    #     lowered_name = searched_book.lower()
    #     lowered_title = all_books_name[i].lower()
    #     if lowered_name in  lowered_title:
    #         res.add(all_books_name[i])
    
    res = sorted(list(res))
    return HttpResponse("\n".join(res))
    
def get_books(request):
    books = Book.objects.all()
    for b in books:
        print(b)
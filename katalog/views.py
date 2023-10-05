from django.shortcuts import render
import pandas as pd
from .models import Book
from django.http import HttpResponse
from proyekts.settings import BASE_DIR
import os
import time
# Create your views here.

# USER GAK BOLEH AKSES
def make_book_dataframe(request):
    source= os.path.join(BASE_DIR, 'datasets')
    res=""
    book_dataset = pd.read_csv(source+'\\pg_catalog.csv', index_col="Text#", dtype=object)
    
    print(f"{len(book_dataset)} books test:")

    tm = time.time()

    book_list = []
    printed = True
    for row in book_dataset.itertuples():
        name = row.Title
        name = str(name)
        name.replace("\n", " ")
        name.replace("\r", " ")
        book = Book(
            title=name,
            author = row.Authors,
            subject = row.Subjects
        )
        book_list.append(book)

        res+=str(book)+"\n"
    
    print(f"pandas took {time.time() - tm} seconds")
    tm = time.time()

    Book.objects.bulk_create(book_list)

    print(f"django took {time.time() - tm} seconds")

    return HttpResponse(res, content_type="text/plain")
    
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

    return HttpResponse("OK")
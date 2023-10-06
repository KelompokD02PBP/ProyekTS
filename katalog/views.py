from django.shortcuts import render
import pandas as pd
from .models import Book
from django.http import HttpResponse
from proyekts.settings import BASE_DIR
import os
import time
import re
# Create your views here.

def aaaa_create_book(row, book_list, res_list):
    name = str(row.Title)

    book = Book(
        title=name,
        author = row.Authors,
        subject = row.Subjects
    )
    
    book_list.append(book)
    res_list.append(str(book))

# USER GAK BOLEH AKSES
def make_book_dataframe(request):
    source= os.path.join(BASE_DIR, 'datasets\\Books')
    res=""
    book_dataset = pd.read_csv(source+'\\Books.csv', index_col="Text#", dtype=object)
    
    print(f"{len(book_dataset)} books test:")

    tm = time.time()

    book_list = []
    res_list = []
    book_dataset.apply(
        lambda row,book_list,res_list: aaaa_create_book(row, book_list,res_list),
        axis=1,
        book_list=book_list,
        res_list=res_list)
    
    print(f"pandas took {time.time() - tm} seconds")
    tm = time.time()

    Book.objects.bulk_create(book_list)

    print(f"django took {time.time() - tm} seconds")

    return HttpResponse('\n'.join(res_list), content_type="text/plain")


def search_book(request, searched_book):
    tm = time.time()
    if 'last_searched' in request.session:
        if searched_book.lower() in request.session['last_searched'].keys():
            print(f"searchmemo {searched_book} took {time.time() - tm} seconds")
            return HttpResponse(request.session['last_searched'][searched_book.lower()])
    else:
        request.session['last_searched']={}

    all_books = Book.objects.all()
    all_books_name = [(str(b.title).lower(), str(b.author).lower()) for b in all_books]
    res=set()
    name_split = searched_book.split(" ")
    searched_book = searched_book.lower()
    # print(all_books_name)

    regex_to_search = rf".*{searched_book}.*"
    regex_to_search_start = rf"${searched_book}.*"
    regex_to_search_end = rf".*{searched_book}^"

    index = 0

    for tuple in all_books_name:

        match = searched_book in tuple[0] or searched_book in tuple[1] or bool(re.search(regex_to_search, tuple[0])) or bool(re.search(regex_to_search, tuple[1]))\
                or bool(re.search(regex_to_search_start, tuple[0])) or bool(re.search(regex_to_search_start, tuple[1]))\
                or bool(re.search(regex_to_search_end, tuple[0])) or bool(re.search(regex_to_search_end, tuple[1]))
        if(match):
            res.add(all_books[index])
        index+=1
    print(f"search {searched_book} took {time.time() - tm} seconds") #12.358 second #10.57
    found_books = ""

    for b in res:
        found_books+=str(b)+"\n"

    dic = request.session['last_searched']
    dic[searched_book]=found_books

    request.session.modified=True

    # print(request.session['last_searched'])
    
    return HttpResponse(found_books)
    
def get_books(request):
    books = Book.objects.all()
    for b in books:
        print(b)

    return HttpResponse("OK")
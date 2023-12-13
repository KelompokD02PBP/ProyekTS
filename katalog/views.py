import json
from django.shortcuts import render
from .models import Book
from django.http import HttpResponse
from proyekts.settings import BASE_DIR
import pandas as pd
import csv
import os
import time
import re
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers

# USER GAK BOLEH AKSES
# Deprecated, see katalog.migrations.0002
# def make_book_dataframe(request):
#     source= os.path.join(BASE_DIR, 'datasets\\Books.csv')
#     print("all books test:")

#     tm = time.time()

#     book_list = []
#     res_list = []
#     with open(source+'/Books.csv', newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             book = Book(
#                 isbn = row['ISBN'],
#                 title = row["Book-Title"].replace("\n", " ").replace("\r"," "),
#                 author = row["Book-Author"],
#                 # subject = row["Subjects"]
#                 year_of_publish = row['Year-Of-Publication'],
#                 publisher = row['Publisher'],
#                 image_url_s = row['Image-URL-S'],
#                 image_url_m = row['Image-URL-M'],
#                 image_url_l = row['Image-URL-L']
#             )
#             book_list.append(book)
#             res_list.append(str(book))
    
#     print(f"csv took {time.time() - tm} seconds")
#     tm = time.time()

#     Book.objects.bulk_create(book_list)

#     print(f"django took {time.time() - tm} seconds")

#     return HttpResponse('\n'.join(res_list), content_type="text/plain")

# Deprecated, see search_book2()
# def search_book(searched_book):
#     tm = time.time()
#     # if 'last_searched' in request.session:
#         # if searched_book.lower() in request.session['last_searched'].keys():
#         #     print(f"searchmemo {searched_book} took {time.time() - tm} seconds")
#         #     return HttpResponse(request.session['last_searched'][searched_book.lower()])
#     # else:
#     #     request.session['last_searched']={}

#     all_books = Book.objects.all()
#     all_books_name = [(str(b.title).lower(), str(b.author).lower()) for b in all_books]
#     res=set()
#     name_split = searched_book.split(" ")
#     searched_book = searched_book.lower()
#     # print(all_books_name)

#     regex_to_search = rf".*{searched_book}.*"
#     regex_to_search_start = rf"${searched_book}.*"
#     regex_to_search_end = rf".*{searched_book}^"

#     index = 0

#     for book_tuple in all_books_name:
#         match = searched_book in book_tuple[0] or searched_book in book_tuple[1] or bool(re.search(regex_to_search, book_tuple[0])) or bool(re.search(regex_to_search, book_tuple[1]))\
#                 or bool(re.search(regex_to_search_start, book_tuple[0])) or bool(re.search(regex_to_search_start, book_tuple[1]))\
#                 or bool(re.search(regex_to_search_end, book_tuple[0])) or bool(re.search(regex_to_search_end, book_tuple[1]))
#         if(match):
#             res.add(all_books[index])
#         index+=1
#     print(f"search {searched_book} took {time.time() - tm} seconds") #12.358 second #10.57
#     # found_books = ""

#     # for b in res:
#         # found_books+=(str(b)+"\n\n")


#     # dic = request.session['last_searched']
#     # dic[searched_book]=found_books

#     # request.session.modified=True

#     # # print(request.session['last_searched'])
    
#     # return HttpResponse(found_books, content_type="text/plain")
#     return res

def search_book2(book):
    # tm = time.time() 
    # HOLY SHIT INI KENCENG BANGET
    books = Book.objects.filter(title__istartswith=book)| Book.objects.filter(title__iendswith=book) | Book.objects.filter(title__icontains=book)
    
    # print(f"search took {time.time() - tm} seconds")
    return books

def get_books(request):
    books = Book.objects.all()
    res_list = []
    
    for b in books:
        res_list.append(str(b))

    return HttpResponse("\n".join(res_list), content_type="text/plain")

def get_books_json(request):
    books = Book.objects.all()
    books = books[:100]

    return HttpResponse(serializers.serialize('json',books), content_type="application/json")

def get_search_book_json(request, book_name):
    tm = time.time() 
    # HOLY SHIT INI KENCENG BANGET

    books = Book.objects.filter(title__istartswith=book_name)| Book.objects.filter(title__iendswith=book_name) | Book.objects.filter(title__icontains=book_name)

    
    return HttpResponse(serializers.serialize('json',books), content_type="application/json")

@csrf_exempt
def get_sorted_book_json(request, book_name=""):
    order_by=""
    if request.method == 'POST':
        # order_by_value = request.POST.get('order_by')
        order_by_value = json.loads(request.body)
        order_by_value = order_by_value['order_by']
        print("order by val :",order_by_value)
        if order_by_value == '1':
            order_by = "asc"
        elif order_by_value == '2':
            order_by = "desc"
        elif order_by_value == '3':
            order_by = "year_asc"
        elif order_by_value == '4':
            order_by = "year_desc"
        elif order_by_value == '5':
            order_by = "atas_2000"
        elif order_by_value == '6':
            order_by = "bawah_2000"
        else:
            order_by = request.GET.get('order_by', 'asc')
    else:
        order_by = request.GET.get('order_by', 'asc')
        
    if order_by == 'asc' or order_by==None:
        books = Book.objects.filter(title__istartswith=book_name)| Book.objects.filter(title__iendswith=book_name) | Book.objects.filter(title__icontains=book_name).order_by("title")
    elif order_by =='desc':
        books = Book.objects.filter(title__istartswith=book_name)| Book.objects.filter(title__iendswith=book_name) | Book.objects.filter(title__icontains=book_name).order_by("-title")
    elif order_by == "year_asc":
        books = Book.objects.filter(title__istartswith=book_name)| Book.objects.filter(title__iendswith=book_name) | Book.objects.filter(title__icontains=book_name).order_by("year_of_publish")
    elif order_by == "year_desc":
        books = Book.objects.filter(title__istartswith=book_name)| Book.objects.filter(title__iendswith=book_name) | Book.objects.filter(title__icontains=book_name).order_by("-year_of_publish")
    elif order_by == "atas_2000":
        books = Book.objects.filter(title__istartswith=book_name, year_of_publish__gte=2000) | Book.objects.filter(title__icontains=book_name, year_of_publish__gte=2000) | Book.objects.filter(title__iendswith=book_name, year_of_publish__gte=2000)
    elif order_by == "bawah_2000":
        books = Book.objects.filter(title__istartswith=book_name, year_of_publish__lt=2000) | Book.objects.filter(title__icontains=book_name, year_of_publish__lt=2000) | Book.objects.filter(title__iendswith=book_name, year_of_publish__lt=2000)

    sorted_books = books
    sorted_books = sorted_books[:100]
    
    return HttpResponse(serializers.serialize('json',sorted_books), content_type="application/json")

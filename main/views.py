import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from katalog.models import Book, AppUser
from katalog.views import search_book2
from .models import Like

from django.core import serializers

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login')
def show_main(request):
    context = {}
    
    if request.user:
        context['name'] = request.user.username
        context['page_num']=-1 #Kalo blm login gk bisa ngapa-ngapain

        if request.user.id !=None: #Kalo udh login bisa liat halaman
            context['page_num']=1
            context['books']=get_katalog(1,order_by=request.GET.get('order_by'))

    return render(request, "main.html", context)



def show_main_page(request, page_num):
    context = {}
    
    if request.user:
        context['name'] = request.user.username
        if(page_num<=0):
            page_num=1
        context['books']=get_katalog(page_num, order_by=request.GET.get('order_by'))
        context['page_num'] = page_num

    return render(request, "main.html", context)

'''
Show main jika search
'''
books_last_searched=[] #simpen search sebelumnya biar bisa next/prior page dengan cepat
last_searched="" #simpen kata yang di search terakhir

def show_main_search(request, page_num):
    global books_last_searched
    global last_searched
    context = {}
    order_by  = request.GET.get('order_by')
    to_find = request.GET.get("search_bar")
    print("last_searched:",last_searched)
        
    if request.user:
        context['name'] = request.user.username
        if(page_num<=0):
            page_num=1
        context['page_num'] = page_num
        context['from_search']=True
        
        #search string kosong
        if to_find!=None and len(to_find)==0 and last_sort_by==order_by:
            return HttpResponseRedirect(reverse("main:show_main_page", kwargs={'page_num':1}))

        # yang dicari beda lagi, kosongin list sebelumnya
        # to_find!=None buat pastiin bukan gr gr refresh/nextpage
        if to_find!=None and last_searched!=to_find:
            books_last_searched=[]
            last_searched=""
        
        
        # kalo blm pernah search atau search hal baru
        if len(books_last_searched)==0:
            books = search_katalog(to_find, page_num,order_by=request.GET.get('order_by'))
            context['books'] = books

        # ganti page
        else:
            books = search_katalog(last_searched, page_num,order_by=request.GET.get('order_by'))

            #Next page tapi udh habis
            if(len(books)==0):
                books = search_katalog(last_searched, page_num-1,order_by=request.GET.get('order_by'))
                context['page_num']=page_num-1
            context['books'] = books
    #   
    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main_page", kwargs={'page_num':1}))
            response.set_cookie('last_login', str(datetime.datetime.now()), max_age=10000)
            messages.success(request, 'Hello ' + user.username + "!")
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def get_katalog(page_num,order_by):
    result=[]
    print(order_by)
    if order_by == 'asc' or order_by==None:
        books = Book.objects.all().order_by("title")
    elif order_by =='desc':
        books = Book.objects.all().order_by("-title")
    elif order_by == "year_asc":
        books = Book.objects.all().order_by("year_of_publish")
    elif order_by == "year_desc":
        books = Book.objects.all().order_by("-year_of_publish")
    elif order_by == "atas_2000":
        books = Book.objects.filter(year_of_publish__gte=2000)
    elif order_by == "bawah_2000":
        books = Book.objects.filter(year_of_publish__lt=2000)
    i=page_num*20-20
    while(i<page_num*20 and i<len(books)):
        result+=[books[i]]
        i+=1

    return result


'''
membuat daftar yang dicari
'''
last_sort_by = ""
def search_katalog(to_find ,page_num,order_by):
    global books_last_searched
    global last_searched
    global last_sort_by
    # search hal baru
    if len(books_last_searched)==0 or order_by!=last_sort_by:
        result=[]
        
        if order_by=='asc' or order_by == None:
            books = list(search_book2(to_find).order_by("title"))
        else:
            books = list(search_book2(to_find).order_by("-title"))
            
        i=page_num*20-20

        books_last_searched = books
        last_searched = to_find
        last_sort_by = order_by
        while(i<len(books) and i<page_num*20):
            result.append(books[i])
            i+=1

    # ganti page
    else:
        result=[]
        books = books_last_searched
        
        i=page_num*20-20

        while(i<len(books) and i<page_num*20):
            result.append(books[i])
            i+=1

    return result


# Ke page per buku
def book_review(request, id):
    context={}
    if request.user:
        book = Book.objects.get(pk=id)
        context['book']=book
        context['name'] = request.user.username
        context['id'] = request.user.pk
    return render(request, 'book.html', context)

@csrf_exempt
def add_like_ajax(request):
    # print("in add_like_ajax views.py")
    if request.method == 'POST':
        id = request.POST.get("id")
        book = Book.objects.get(pk=id)

        has_like = Like.objects.filter(book = book, user = request.user)
        print("has like =",has_like)

        print("anjing", book, request.user)
        if len(has_like)==0:
            like = Like(user = request.user,
                        book = book
                        )
            print("like",like)
            like.save()
        else:
            has_like.delete()

        return HttpResponse(b"LIKED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def see_like_ajax(request):
    print("in add_like_ajax views.py")
    if request.method == 'POST':
        id = request.POST.get("id")
        print("id",id)
        book = Book.objects.get(pk=id)
        likes = Like.objects.filter(book=book)
        # print("likes", type(likes))

        return HttpResponse(serializers.serialize('json',likes))
    return HttpResponseNotFound()

@csrf_exempt
def like_dislike_ajax(request):
    print("in like_dislike views.py")
    if request.method == 'POST':
        id = request.POST.get("id")
        book = Book.objects.get(pk=id)
        print("book in like_dislike",book)
        likes = Like.objects.filter(book=book, user = request.user)
        print(len(likes))
        if len(likes)==1:
            print("like")
            print(likes)
        else:
            print("dislike")
            print(likes)
        return HttpResponse(serializers.serialize('json',likes))
    return HttpResponseNotFound()

@csrf_exempt
def sort_books_ajax(request,page_num,order_by):
    sorted_books = get_katalog(page_num,order_by)
    return HttpResponse(serializers.serialize('json',sorted_books))

@csrf_exempt
def sort_books_ajax_search(request,page_num,order_by):
    sorted_books = search_katalog(last_searched, page_num,order_by)
    return HttpResponse(serializers.serialize('json',sorted_books))
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse

from katalog.models import Book, AppUser
from katalog.views import search_book

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

def show_main(request):
    context = {}
    
    if request.user:
        context['name'] = request.user.username
        context['page_num']=-1 #Kalo blm login gk bisa ngapa-ngapain

        if request.user.id !=None: #Kalo udh login bisa liat halaman
            context['page_num']=1
            context['books']=get_katalog(1)

    return render(request, "main.html", context)

def show_main_page(request, page_num):
    context = {}
    
    if request.user:
        context['name'] = request.user.username
        context['books'] = get_katalog(page_num)
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

    # MASIH ERROR DI BAGIAN RE-SEARCH
    to_find = request.GET.get("search_bar")
    print("last_searched:",last_searched)
        
    if request.user:
        context['name'] = request.user.username
        context['page_num'] = page_num
        context['from_search']=True
        
        # yang dicari beda lagi, kosongin list sebelumnya
        # to_find!=None buat pastiin bukan gr gr refresh/nextpage

        if to_find!=None and len(to_find)==0:
            return HttpResponseRedirect(reverse("main:show_main_page", kwargs={'page_num':1}))

        if to_find!=None and last_searched!=to_find:
            books_last_searched=[]
            last_searched=""
        
        # kalo blm pernah search atau search hal baru
        if len(books_last_searched)==0:
            books = search_katalog(to_find, page_num)
            context['books'] = books

            request.session.modified=True
        # ganti page
        else:
            books = search_katalog("", page_num)
            context['books'] = books

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

def get_katalog(page_num):
    result=[]
    books = Book.objects.all()
    for i in range (page_num*100-100, page_num*100):
        result+=[books[i]]
        
    return result

'''
membuat daftar yang dicari
'''
def search_katalog(to_find ,page_num):
    global books_last_searched
    global last_searched
    
    # search hal baru
    if len(books_last_searched)==0:
        result=[]
        books = list(search_book(to_find))
        i=page_num*100-100

        books_last_searched = books
        last_searched = to_find
        while(i<len(books) and i<page_num*100):
            result.append(books[i])
            i+=1

    # ganti page
    else:
        result=[]
        books = books_last_searched
        i=page_num*100-100
        # print("book: ",books)

        while(i<len(books) and i<page_num*100):
            result.append(books[i])
            i+=1

    return result

def book_review(request, id):
    context={}
    book = Book.objects.get(pk=id)
    context['book']=book
    return render(request, 'book.html', context)

@csrf_exempt
def add_like_ajax(request):
    print("in add_like_ajax views.py")
    if request.method == 'POST':
        id = request.POST.get("id")
        book = Book.objects.get(pk=id)
        print(book)
        
        return HttpResponse(b"LIKED", status=201)
    return HttpResponseNotFound()